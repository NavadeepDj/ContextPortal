from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.core.retriever import (
    MAX_HTTP_RETRIES,
    AccessDeniedError,
    AuthenticationRequiredError,
    ContextResult,
    FetchError,
    _extract_content,
    _fetch_authenticated_sync,
    extract_markdown,
    fetch_authenticated,
    fetch_public,
    get_context,
)


@pytest.mark.asyncio
async def test_extract_markdown():
    html = """
    <html>
        <head><title>Test Document</title></head>
        <body>
            <script>console.log('Malicious or tracker script');</script>
            <h1>Main Title</h1>
            <p>This is a paragraph with <strong>bold</strong> text.</p>
            <style>body { color: red; }</style>
        </body>
    </html>
    """
    md, title = await extract_markdown(html)
    assert "# Main Title" in md
    assert "This is a paragraph with **bold** text." in md
    assert "Malicious or tracker script" not in md
    assert "color: red;" not in md


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_public_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.url = "https://example.com/Docs/Article?next=/login&sig=AbC"
    mock_response.headers = {"content-type": "text/html; charset=utf-8"}
    mock_response.text = "<html><body><h1>Sample Article</h1><p>Here is a detailed article with plenty of content to pass the minimum character count check.</p></body></html>"
    mock_get.return_value = mock_response

    result = await fetch_public("https://example.com/article")
    assert result is not None
    assert result.retrieval_method == "http"
    assert result.authenticated is False
    assert result.url == mock_response.url
    assert "# Sample Article" in result.content


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_public_unauthorized_status(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_get.return_value = mock_response

    result = await fetch_public("https://example.com/protected")
    assert result is None


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_public_forbidden_status(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_get.return_value = mock_response

    result = await fetch_public("https://example.com/forbidden")
    assert result is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "login_url",
    ["https://example.com/login?redirect=/protected", "https://sso.example.com/access"],
)
@patch("httpx.AsyncClient.get")
async def test_fetch_public_auth_redirect(mock_get, login_url):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.url = login_url
    mock_response.headers = {"content-type": "text/html"}
    mock_response.text = "<html><body><h1>Login</h1></body></html>"
    mock_get.return_value = mock_response

    result = await fetch_public("https://example.com/protected")
    assert result is None


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_public_does_not_return_same_url_login_form(mock_get):
    url = "https://example.com/Private"
    mock_get.return_value = httpx.Response(
        200,
        request=httpx.Request("GET", url),
        headers={"content-type": "text/html"},
        text="<h1>Sign in to your account</h1>"
        + "<p>Sign in to continue to the requested resource.</p>" * 5
        + '<form><input type="password"></form>',
    )

    assert await fetch_public(url) is None


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_public_empty_spa_shell(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.url = "https://example.com/app"
    mock_response.headers = {"content-type": "text/html"}
    mock_response.text = "<html><body><div id='root'></div></body></html>"
    mock_get.return_value = mock_response

    result = await fetch_public("https://example.com/app")
    assert result is None


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_public_non_html(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.url = "https://example.com/data.json"
    mock_response.headers = {"content-type": "application/json"}
    mock_response.text = '{"status": "ok", "message": "hello"}'
    mock_get.return_value = mock_response

    result = await fetch_public("https://example.com/data.json")
    assert result.content == '{"status": "ok", "message": "hello"}'


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_public_exception(mock_get, caplog):
    url = "https://user:SECRET@example.com/PRIVATE?token=SECRET#SECRET"
    mock_get.side_effect = httpx.ConnectError(f"Failed to connect to {url}")
    with caplog.at_level("INFO", logger="app.core.retriever"):
        result = await fetch_public(url)
    assert result is None
    assert "Public fetch failed" in caplog.text
    assert "SECRET" not in caplog.text
    assert "PRIVATE" not in caplog.text


@pytest.mark.asyncio
@patch("app.core.retriever._fetch_public")
@patch("app.core.retriever.fetch_authenticated")
async def test_get_context_public_branch(mock_fetch_auth, mock_fetch_public):
    from app.core.retriever import ContextResult

    mock_fetch_public.return_value = ContextResult(
        url="https://example.com",
        title=None,
        content="# Public Markdown",
        retrieval_method="http",
        authenticated=False,
    )

    result = await get_context("https://example.com")
    assert result.content == "# Public Markdown"
    mock_fetch_public.assert_called_once_with("https://example.com")
    mock_fetch_auth.assert_not_called()


@pytest.mark.asyncio
@patch("app.core.retriever._fetch_public")
@patch("app.core.retriever.fetch_authenticated")
async def test_get_context_fallback_to_authenticated(
    mock_fetch_auth, mock_fetch_public
):
    mock_fetch_public.return_value = None
    mock_fetch_auth.return_value = ContextResult(
        url="https://example.com/protected",
        title=None,
        content="# Browser Context",
        retrieval_method="browser",
        authenticated=None,
    )

    result = await get_context("https://example.com/protected")
    assert result.content == "# Browser Context"
    assert result.authenticated is None
    mock_fetch_public.assert_called_once_with("https://example.com/protected")
    mock_fetch_auth.assert_called_once_with("https://example.com/protected")


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
@patch("app.core.retriever.fetch_authenticated")
async def test_get_context_confirms_browser_success_after_public_401(
    mock_browser, mock_get
):
    url = "https://example.com/Private"
    mock_get.return_value = httpx.Response(401)
    mock_browser.return_value = ContextResult(
        url=url,
        content="Private content",
        retrieval_method="browser",
        authenticated=None,
    )

    result = await get_context(url)

    assert result.authenticated is True
    assert result.url == url


@pytest.mark.asyncio
@patch("app.core.retriever._fetch_authenticated_sync")
async def test_fetch_authenticated_thread_delegation(mock_sync_fetch):
    mock_sync_fetch.return_value = ContextResult(
        url="https://example.com/protected",
        title=None,
        content="# Auth Markdown",
        retrieval_method="browser",
        authenticated=True,
    )
    result = await fetch_authenticated("https://example.com/protected")
    assert result.content == "# Auth Markdown"
    mock_sync_fetch.assert_called_once_with("https://example.com/protected")


@pytest.fixture
def browser_page():
    with patch("app.core.retriever.sync_playwright") as playwright:
        chromium = playwright.return_value.__enter__.return_value.chromium
        context = chromium.launch_persistent_context.return_value
        page = context.new_page.return_value
        page.goto.return_value.status = 200
        page.locator.return_value.count.return_value = 0
        yield page
        context.close.assert_called_once()


def test_fetch_authenticated_sync_without_challenge_is_unverified(browser_page):
    browser_page.url = "https://example.com/Dashboard?token=AbC"
    browser_page.content.return_value = (
        "<html><body><h1>Dashboard</h1><p>Authorized user info</p></body></html>"
    )

    result = _fetch_authenticated_sync(browser_page.url)

    assert "# Dashboard" in result.content
    assert result.authenticated is None
    assert result.url == browser_page.url


def test_fetch_authenticated_sync_with_login_flow(browser_page):
    url = "https://example.com/Protected"
    browser_page.url = "https://sso.example.com/access"
    browser_page.content.return_value = (
        "<html><body><h1>Protected Course</h1><p>Welcome student!</p></body></html>"
    )

    def complete_login(*_):
        browser_page.url = url

    browser_page.wait_for_timeout.side_effect = complete_login
    result = _fetch_authenticated_sync(url)

    assert "# Protected Course" in result.content
    assert result.authenticated is True


@patch("app.core.retriever.LOGIN_POLL_ATTEMPTS", 2)
def test_fetch_authenticated_sync_rejects_lingering_same_url_login(browser_page):
    browser_page.url = "https://example.com/Protected"
    browser_page.locator.return_value.count.return_value = 1

    with pytest.raises(AuthenticationRequiredError):
        _fetch_authenticated_sync(browser_page.url)

    assert browser_page.goto.call_count == 2
    browser_page.content.assert_not_called()


@pytest.mark.parametrize(
    ("status", "error"),
    [(401, AuthenticationRequiredError), (403, AccessDeniedError), (500, FetchError)],
)
def test_fetch_authenticated_sync_rejects_browser_error_status(
    browser_page, status, error
):
    browser_page.url = "https://example.com/Protected"
    browser_page.goto.return_value.status = status

    with pytest.raises(error) as exc:
        _fetch_authenticated_sync(browser_page.url)

    assert type(exc.value) is error
    browser_page.content.assert_not_called()


def test_fetch_authenticated_sync_rejects_denial_after_login(browser_page):
    url = "https://example.com/Protected"
    browser_page.url = "https://sso.example.com/login"

    def redirect_after_login(*_):
        browser_page.url = url
        denied = MagicMock(status=403, frame=browser_page.main_frame)
        browser_page.on.call_args.args[1](denied)

    browser_page.wait_for_timeout.side_effect = redirect_after_login

    with pytest.raises(AccessDeniedError):
        _fetch_authenticated_sync(url)

    browser_page.content.assert_not_called()


# ── new tests for pipeline fixes ──────────────────────────────────────────────


@pytest.mark.asyncio
@patch("asyncio.sleep", new_callable=AsyncMock)
@patch("httpx.AsyncClient.get")
async def test_fetch_public_retries_on_429(mock_get, mock_sleep):
    throttled = MagicMock()
    throttled.status_code = 429

    ok = MagicMock()
    ok.status_code = 200
    ok.url = "https://example.com/article"
    ok.headers = {"content-type": "text/html; charset=utf-8"}
    ok.text = (
        "<html><body><h1>Retried Article</h1>"
        "<p>Content retrieved successfully after a rate-limit retry on the first attempt. "
        "This paragraph contains enough text to pass the minimum content length threshold.</p>"
        "</body></html>"
    )

    mock_get.side_effect = [throttled, ok]

    result = await fetch_public("https://example.com/article")

    assert result is not None
    assert result.retrieval_method == "http"
    assert "# Retried Article" in result.content
    mock_sleep.assert_called_once()


@pytest.mark.asyncio
@patch("asyncio.sleep", new_callable=AsyncMock)
@patch("httpx.AsyncClient.get")
async def test_fetch_public_exhausts_429_retries(mock_get, mock_sleep):
    throttled = MagicMock()
    throttled.status_code = 429
    mock_get.return_value = throttled

    result = await fetch_public("https://example.com/throttled")

    assert result is None
    assert mock_sleep.call_count == MAX_HTTP_RETRIES - 1


@pytest.mark.asyncio
@patch("asyncio.sleep", new_callable=AsyncMock)
@patch("httpx.AsyncClient.get")
async def test_fetch_public_timeout_falls_to_browser_immediately(mock_get, mock_sleep):
    mock_get.side_effect = httpx.TimeoutException("timed out")

    result = await fetch_public("https://example.com/slow")

    assert result is None
    mock_sleep.assert_not_called()


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_public_pdf(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.url = "https://example.com/report.pdf"
    mock_response.headers = {"content-type": "application/pdf"}
    mock_get.return_value = mock_response

    result = await fetch_public("https://example.com/report.pdf")

    assert result is not None
    assert "[PDF file:" in result.content
    assert result.content_type == "application/pdf"


@pytest.mark.asyncio
async def test_extract_markdown_strips_images():
    html = """
    <html><body>
        <h1>Article With Images</h1>
        <img src="https://example.com/photo.jpg" alt="A descriptive photo">
        <p>Text content that matters.</p>
    </body></html>
    """
    md, _ = await extract_markdown(html)
    assert "![" not in md
    assert "Text content that matters." in md


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_public_spa_marker_detection(mock_get):
    # This SPA shell has enough noscript text to pass the 100-char threshold,
    # but the id='app' marker should catch it before extraction.
    spa_html = (
        "<html><body>"
        "<div id='app'></div>"
        "<noscript>Please enable JavaScript to run this application. "
        "JavaScript is required to use all features of this site.</noscript>"
        "</body></html>"
    )
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.url = "https://example.com/spa-app"
    mock_response.headers = {"content-type": "text/html"}
    mock_response.text = spa_html
    mock_get.return_value = mock_response

    result = await fetch_public("https://example.com/spa-app")
    assert result is None


def test_extract_content_deduplication():
    html = (
        "<html><body>"
        "<h1>Shared Extraction</h1>"
        "<img src='https://x.com/img.png' alt='ignored'>"
        "<p>Both HTTP and browser paths use this function.</p>"
        "</body></html>"
    )
    md, title = _extract_content(html)
    assert "# Shared Extraction" in md
    assert "![" not in md
    assert "Both HTTP and browser paths" in md
