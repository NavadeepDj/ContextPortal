"""Extract visuals from the same Chrome page as the Markdown context."""

import asyncio
import ipaddress
import socket
from functools import lru_cache
from typing import Any
from urllib.parse import urldefrag, urlsplit, urlunsplit

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Locator, Page, Request, Response
from pydantic import BaseModel

from app.core.retriever import (
    ContextResult,
    FetchError,
    extract_browser_context,
    open_browser_page,
)
from app.core.security import validate_url_policy

MAX_VISUALS = 6
MAX_VISUAL_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 6 * 1024 * 1024
MAX_IMAGE_PIXELS = 16_000_000
MAX_CANDIDATES = 24
MAX_IMAGE_RESPONSES = 256
VISUAL_SELECTOR = (
    "img:visible, canvas:visible, svg:visible:not(svg *), "
    '[role="img"]:visible:not(img, svg, canvas, :has(img, svg, canvas))'
)
RASTER_SIGNATURES = {
    "image/png": (b"\x89PNG\r\n\x1a\n",),
    "image/jpeg": (b"\xff\xd8\xff",),
    "image/gif": (b"GIF87a", b"GIF89a"),
    "image/webp": (b"RIFF",),
}


class PageVisual(BaseModel):
    data: bytes
    mime_type: str
    label: str


class VisualContext(BaseModel):
    context: ContextResult
    visuals: list[PageVisual]


class VisualURLPolicyError(ValueError):
    """A URL policy failure with a message safe to return to the client."""


def _is_public_ip(address: str) -> bool:
    ip = ipaddress.ip_address(address)
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped is not None:
        ip = ip.ipv4_mapped
    return ip.is_global and not ip.is_multicast


class _BrowserURLPolicy:
    def __init__(self) -> None:
        # Cache only for one browser fetch. Chrome still performs its own resolution.
        self._hostname_is_public = lru_cache(maxsize=128)(self._resolve_public)

    @staticmethod
    def _resolve_public(hostname: str) -> bool:
        addresses = socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)
        return bool(addresses) and all(
            _is_public_ip(str(addr[4][0])) for addr in addresses
        )

    def check(self, url: str) -> None:
        try:
            validate_url_policy(url)
            parsed = urlsplit(url)
        except ValueError as exc:
            raise VisualURLPolicyError(str(exc)) from None
        if parsed.username is not None or parsed.password is not None:
            raise VisualURLPolicyError(
                "URLs containing credentials are forbidden by security policy"
            )
        try:
            allowed = self._hostname_is_public(parsed.hostname or "")
        except (OSError, ValueError):
            raise VisualURLPolicyError(
                "Could not resolve the URL to a public address"
            ) from None
        if not allowed:
            raise VisualURLPolicyError(
                "Access to non-public addresses is forbidden by security policy"
            )

    def attach(self, page: Page) -> None:
        session = page.context.new_cdp_session(page)

        def check_request(event: dict[str, Any]) -> None:
            request_id = {"requestId": event["requestId"]}
            try:
                self.check(event["request"]["url"])
            except ValueError:
                session.send(
                    "Fetch.failRequest",
                    {**request_id, "errorReason": "BlockedByClient"},
                )
            else:
                session.send("Fetch.continueRequest", request_id)

        # Chrome pauses each redirect hop. Playwright route() sees only the initial URL.
        session.on("Fetch.requestPaused", check_request)
        session.send(
            "Fetch.enable",
            {"patterns": [{"urlPattern": "http://*"}, {"urlPattern": "https://*"}]},
        )


def _image_type(response: Response) -> str:
    return response.headers.get("content-type", "").partition(";")[0].strip().lower()


def _track_image(page: Page, response: Response, images: dict[str, Response]) -> None:
    if (
        len(images) >= MAX_IMAGE_RESPONSES
        or not response.ok
        or response.request.resource_type not in {"image", "document"}
        or _image_type(response) not in RASTER_SIGNATURES
        or response.frame != page.main_frame
    ):
        return
    request: Request | None = response.request
    # currentSrc can be the URL before an image CDN redirect.
    while request is not None and len(images) < MAX_IMAGE_RESPONSES:
        images[urldefrag(request.url)[0]] = response
        request = request.redirected_from


def _original_image(
    element: Locator,
    images: dict[str, Response],
    policy: _BrowserURLPolicy,
    budget: int,
) -> PageVisual | None:
    element.scroll_into_view_if_needed(timeout=1_000)
    details = element.evaluate(
        """async img => {
            await Promise.race([img.decode().catch(() => {}), new Promise(r => setTimeout(r, 1000))]);
            return {url: img.currentSrc, alt: img.alt,
                    pixels: img.naturalWidth * img.naturalHeight};
        }""",
        timeout=1_000,
    )
    if not 0 < details["pixels"] <= MAX_IMAGE_PIXELS:
        return None
    response = images.get(urldefrag(details["url"])[0])
    if (
        response is None
        or response.headers.get("content-encoding", "identity") != "identity"
    ):
        return None
    policy.check(response.url)
    peer = response.server_addr()
    if peer is not None and not _is_public_ip(peer["ipAddress"]):
        return None
    if not 0 <= response.request.sizes()["responseBodySize"] <= budget:
        return None
    data = response.body()
    mime_type = _image_type(response)
    valid_signature = data.startswith(RASTER_SIGNATURES[mime_type])
    if mime_type == "image/webp":
        valid_signature = valid_signature and data[8:12] == b"WEBP"
    if len(data) > budget or not valid_signature:
        return None
    alt = " ".join(details["alt"].split())[:180]
    return PageVisual(data=data, mime_type=mime_type, label=alt or "Embedded image")


def _collect_visuals(
    page: Page, images: dict[str, Response], policy: _BrowserURLPolicy
) -> list[PageVisual]:
    main = page.locator('main:visible, [role="main"]:visible, article:visible').first
    visuals = (main if main.count() else page.locator("body")).locator(VISUAL_SELECTOR)
    selected: list[PageVisual] = []
    seen: set[bytes] = set()
    remaining = MAX_TOTAL_BYTES
    for element in visuals.all()[:MAX_CANDIDATES]:
        if len(selected) >= MAX_VISUALS or remaining <= 0:
            break
        budget = min(MAX_VISUAL_BYTES, remaining)
        try:
            box = element.bounding_box(timeout=1_000)
            if box is None or box["width"] < 80 or box["height"] < 50:
                continue
            if element.evaluate("el => el.localName", timeout=1_000) == "img":
                visual = _original_image(element, images, policy, budget)
            elif box["width"] <= 1600 and box["height"] <= 1600:
                screenshot = element.screenshot(type="png", scale="css", timeout=2_000)
                visual = PageVisual(
                    data=screenshot, mime_type="image/png", label="Rendered visual"
                )
            else:
                continue
        except (PlaywrightError, ValueError):
            continue
        if (
            visual is not None
            and len(visual.data) <= budget
            and visual.data not in seen
        ):
            selected.append(visual)
            seen.add(visual.data)
            remaining -= len(visual.data)
    return selected


def _fetch_visual_context_sync(url: str) -> VisualContext:
    policy = _BrowserURLPolicy()
    policy.check(url)
    images: dict[str, Response] = {}

    def prepare(page: Page) -> None:
        policy.attach(page)
        page.on("response", lambda response: _track_image(page, response, images))

    with open_browser_page(url, prepare=prepare, service_workers="block") as (
        page,
        challenged,
    ):
        policy.check(page.url)
        context = extract_browser_context(page, challenged)
        visuals = _collect_visuals(page, images, policy)
        if page.url != context.url or not (context.content or visuals):
            raise FetchError()
        # A visual result needs no signed image URL or query string to be useful.
        source = urlsplit(context.url)
        context.url = urlunsplit((source.scheme, source.netloc, source.path, "", ""))
        return VisualContext(context=context, visuals=visuals)


async def get_visual_context(url: str) -> VisualContext:
    return await asyncio.to_thread(_fetch_visual_context_sync, url)
