import asyncio
import logging
import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Literal
from urllib.parse import urlsplit

import httpx
import markdownify
from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright
from playwright.sync_api import Response as BrowserResponse
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pydantic import BaseModel
from readability import Document

logger = logging.getLogger(__name__)


class FetchError(RuntimeError):
    code = "retrieval_failed"
    message = "Could not retrieve the requested page."

    def __init__(self) -> None:
        super().__init__(self.message)


class AuthenticationRequiredError(FetchError):
    code = "authentication_required"
    message = "Sign-in is required or the session expired. Run `contextportal login` and retry."


class AccessDeniedError(FetchError):
    code = "access_denied"
    message = (
        "The site denied access. Check that the signed-in account can open the page."
    )


class ContextResult(BaseModel):
    url: str
    title: str | None = None
    content: str
    content_type: str = "text/markdown"
    retrieval_method: str
    # None means the browser rendered content without evidence of a recovered session.
    authenticated: bool | None

    @property
    def authentication_label(self) -> str:
        return "Unverified" if self.authenticated is None else str(self.authenticated)


# ── constants ─────────────────────────────────────────────────────────────────

USER_AGENT = "ContextPortal/0.1.0 (+https://github.com/NavadeepDj/ContextPortal)"

# 1 retry (initial attempt + 1 backoff) for genuine server-overload signals only.
# Timeouts fall through to the browser immediately — retrying a timeout just adds
# latency before the Playwright fallback, which is the right tool for slow/auth-gated sites.
# See decisions/ADR-004-http-retry-strategy.md for the full rationale.
MAX_HTTP_RETRIES = 2
RETRY_ON_STATUS = {429, 503}
MIN_CONTENT_CHARS = 100
LOGIN_PATH_SEGMENTS = {"login", "signin", "sign-in", "oauth", "oauth2", "sso", "saml"}
LOGIN_POLL_INTERVAL_MS = 2_000
LOGIN_POLL_ATTEMPTS = 150

# Patterns in raw HTML that indicate a JavaScript-only SPA shell with no real content.
# Checked before extraction to catch shells whose error/loading text passes the char threshold.
SPA_MARKERS = [
    'id="root"',
    "id='root'",
    'id="app"',
    "id='app'",
    "you need to enable javascript",
    "please enable javascript",
    "this site requires javascript",
]


# ── shared extraction helper ───────────────────────────────────────────────────


def _extract_content(html: str) -> tuple[str, str]:
    """Single source of truth: HTML → (markdown, title)."""
    doc = Document(html)
    title = doc.title()
    main_html = doc.summary()
    soup = BeautifulSoup(main_html, "lxml")
    md = markdownify.markdownify(
        str(soup), heading_style="ATX", strip=["script", "style", "img"]
    )
    md = "\n".join([line for line in md.splitlines() if line.strip() or line == ""])
    return md.strip(), title


async def extract_markdown(html: str) -> tuple[str, str]:
    """Async shim kept for backwards compatibility — delegates to _extract_content."""
    return _extract_content(html)


# ── HTTP fetch ────────────────────────────────────────────────────────────────


async def fetch_public(url: str) -> ContextResult | None:
    """Attempts to fetch the URL normally. Returns ContextResult if successful and not blocked, else None."""
    try:
        return await _fetch_public(url)
    except AuthenticationRequiredError:
        return None


async def _fetch_public(url: str) -> ContextResult | None:
    headers = {"User-Agent": USER_AGENT}
    try:
        async with httpx.AsyncClient(
            headers=headers, follow_redirects=True, timeout=10.0
        ) as client:
            for attempt in range(MAX_HTTP_RETRIES):
                try:
                    response = await client.get(url)
                except httpx.TimeoutException:
                    logger.info("Public fetch timed out. Trying the browser.")
                    return None
                if response.status_code == 401:
                    raise AuthenticationRequiredError()
                if response.status_code == 403:
                    logger.info("Public fetch hit HTTP 403.")
                    return None

                if response.status_code in RETRY_ON_STATUS:
                    if attempt < MAX_HTTP_RETRIES - 1:
                        logger.info(
                            "HTTP %s. Retrying public fetch in %ss.",
                            response.status_code,
                            2**attempt,
                        )
                        await asyncio.sleep(2**attempt)
                        continue
                    logger.info(
                        "Public fetch hit HTTP %s after retries.", response.status_code
                    )
                    return None

                response.raise_for_status()

                final_url = str(response.url)
                if _is_login_url(final_url, url):
                    raise AuthenticationRequiredError()

                content_type = response.headers.get("content-type", "")

                if "application/pdf" in content_type:
                    return ContextResult(
                        url=final_url,
                        title=None,
                        content=(
                            "[PDF file: direct text extraction is not supported. "
                            "Download the file and use a dedicated PDF reader.]"
                        ),
                        content_type=content_type,
                        retrieval_method="http",
                        authenticated=False,
                    )

                if "text/html" not in content_type:
                    return ContextResult(
                        url=final_url,
                        title=None,
                        content=response.text,
                        content_type=content_type,
                        retrieval_method="http",
                        authenticated=False,
                    )

                # Detect SPA shells before running the full extraction pipeline
                raw_lower = response.text.lower()
                if "password" in raw_lower and BeautifulSoup(
                    response.text, "lxml"
                ).select_one(
                    'form input[type="password" i]:not([hidden], [hidden] *, template *)'
                ):
                    raise AuthenticationRequiredError()
                if any(marker in raw_lower for marker in SPA_MARKERS):
                    logger.info("SPA shell markers detected in public fetch.")
                    return None

                md, title = await extract_markdown(response.text)

                if len(md.strip()) < MIN_CONTENT_CHARS:
                    logger.info("Public fetch returned too little content.")
                    return None

                return ContextResult(
                    url=final_url,
                    title=title,
                    content=md,
                    content_type="text/markdown",
                    retrieval_method="http",
                    authenticated=False,
                )

    except AuthenticationRequiredError:
        raise
    except Exception:
        logger.info("Public fetch failed.")
        return None

    return None


# ── browser auth helpers ──────────────────────────────────────────────────────


def _is_login_url(url: str, target_url: str) -> bool:
    segments = urlsplit(url).path.lower().strip("/").split("/")
    if segments[-1] == "access":
        # Some SSO providers use an access gateway on a different origin.
        return not _same_origin(url, target_url)
    return segments[-1] == "auth" or bool(LOGIN_PATH_SEGMENTS.intersection(segments))


def _has_login_challenge(page: Page, target_url: str) -> bool:
    return _is_login_url(page.url, target_url) or bool(
        page.locator('input[type="password" i]:visible').count()
    )


def _same_origin(first_url: str, second_url: str) -> bool:
    first = httpx.URL(first_url)
    second = httpx.URL(second_url)
    return (first.scheme, first.netloc) == (second.scheme, second.netloc)


def _check_browser_response(response: BrowserResponse | None) -> None:
    if response is None:
        return
    if response.status == 401:
        raise AuthenticationRequiredError()
    if response.status == 403:
        raise AccessDeniedError()
    if response.status >= 400:
        raise FetchError()


@contextmanager
def open_browser_page(
    url: str,
    *,
    prepare: Callable[[Page], None] | None = None,
    service_workers: Literal["allow", "block"] = "allow",
) -> Iterator[tuple[Page, bool]]:
    """
    Sync function that runs Playwright in a thread.
    Uses sync_api to avoid the Windows asyncio subprocess bug.

    Handles OAuth popup flows (e.g. Google Sign-In) by polling the
    main page's URL rather than watching for DOM changes on the page,
    since OAuth opens new windows that we can't inspect.
    """
    # Use a deterministic global directory for the user profile so it persists across different CWDs
    from pathlib import Path

    user_data_dir = str(Path.home() / ".contextportal" / "playwright_profile")

    with sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1280, "height": 800},
            service_workers=service_workers,
        )

        try:
            page = browser_context.new_page()
            if prepare is not None:
                prepare(page)
            last_response: BrowserResponse | None = None

            def track_navigation(response: BrowserResponse) -> None:
                nonlocal last_response
                if (
                    response.request.is_navigation_request()
                    and response.frame == page.main_frame
                ):
                    last_response = response

            def wait_for_page(timeout: int) -> None:
                try:
                    page.wait_for_load_state("networkidle", timeout=timeout)
                except PlaywrightTimeoutError:
                    pass

            def navigate(timeout: int) -> None:
                nonlocal last_response
                last_response = None
                response = page.goto(url, wait_until="domcontentloaded")
                if last_response is None:
                    last_response = response
                wait_for_page(timeout)

            page.on("response", track_navigation)
            navigate(timeout=5000)
            challenged = _has_login_challenge(page, url)
            if not challenged or (
                last_response is not None and last_response.status != 401
            ):
                _check_browser_response(last_response)

            if challenged:
                print(
                    "Sign-in required. Complete login in the browser window within 5 minutes.",
                    file=sys.stderr,
                )
                for _ in range(LOGIN_POLL_ATTEMPTS):
                    page.wait_for_timeout(LOGIN_POLL_INTERVAL_MS)
                    if last_response is not None and last_response.status == 403:
                        raise AccessDeniedError()
                    if _same_origin(page.url, url) and not _has_login_challenge(
                        page, url
                    ):
                        break
                if (
                    page.url != url
                    or _has_login_challenge(page, url)
                    or (last_response is not None and last_response.status == 401)
                ):
                    # A popup can set the session without returning the main page to the target.
                    navigate(timeout=10000)
                else:
                    wait_for_page(timeout=10000)
                _check_browser_response(last_response)
                if not _same_origin(page.url, url) or _has_login_challenge(page, url):
                    raise AuthenticationRequiredError()

            yield page, challenged

        finally:
            browser_context.close()


def extract_browser_context(page: Page, challenged: bool) -> ContextResult:
    """Extract Markdown and source metadata from the current browser document."""
    md_content, title = _extract_content(page.content())
    return ContextResult(
        url=page.url,
        title=title,
        content=md_content,
        retrieval_method="browser",
        authenticated=True if challenged else None,
    )


def _fetch_authenticated_sync(url: str) -> ContextResult:
    with open_browser_page(url) as (page, challenged):
        result = extract_browser_context(page, challenged)
        if not result.content:
            raise FetchError()
        return result


async def fetch_authenticated(url: str) -> ContextResult:
    """Runs Playwright in a background thread to avoid Windows asyncio issues."""
    return await asyncio.to_thread(_fetch_authenticated_sync, url)


async def get_context(url: str) -> ContextResult:
    """Main entrypoint: tries public fetch, falls back to authenticated fetch."""
    public_challenge = False
    try:
        public_result = await _fetch_public(url)
        if public_result is not None:
            return public_result
    except AuthenticationRequiredError:
        public_challenge = True

    logger.info("Trying the saved browser session.")
    try:
        result = await fetch_authenticated(url)
        if public_challenge and _same_origin(result.url, url):
            result.authenticated = True
        return result
    except FetchError:
        raise
    except Exception:
        raise FetchError() from None
