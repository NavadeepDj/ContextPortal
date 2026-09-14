from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from app.core.retriever import (
    ContextResult,
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
    mock_response.url = "https://example.com/article"
    mock_response.headers = {"content-type": "text/html; charset=utf-8"}
    mock_response.text = "<html><body><h1>Sample Article</h1><p>Here is a detailed article with plenty of content to pass the minimum character count check.</p></body></html>"
    mock_get.return_value = mock_response

    result = await fetch_public("https://example.com/article")
    assert result is not None
    assert result.retrieval_method == "http"
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
@patch("httpx.AsyncClient.get")
async def test_fetch_public_auth_redirect(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.url = "https://example.com/login?redirect=/protected"
    mock_response.headers = {"content-type": "text/html"}
    mock_response.text = "<html><body><h1>Login</h1></body></html>"
    mock_get.return_value = mock_response

    result = await fetch_public("https://example.com/protected")
    assert result is None


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
async def test_fetch_public_exception(mock_get):
    mock_get.side_effect = Exception("Connection timed out")

    result = await fetch_public("https://unreachable.example.com")
    assert result is None


@pytest.mark.asyncio
@patch("app.core.retriever.fetch_public")
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
@patch("app.core.retriever.fetch_public")
@patch("app.core.retriever.fetch_authenticated")
async def test_get_context_fallback_to_authenticated(
    mock_fetch_auth, mock_fetch_public
):
    mock_fetch_public.return_value = None
    mock_fetch_auth.return_value = ContextResult(
        url="https://example.com/protected",
        title=None,
        content="# Authenticated Context",
        retrieval_method="browser",
        authenticated=True,
    )

    result = await get_context("https://example.com/protected")
    assert result.content == "# Authenticated Context"
    mock_fetch_public.assert_called_once_with("https://example.com/protected")
    mock_fetch_auth.assert_called_once_with("https://example.com/protected")


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


@patch("app.core.retriever.sync_playwright")
def test_fetch_authenticated_sync_already_authenticated(mock_sync_playwright):
    from app.core.retriever import _fetch_authenticated_sync

    mock_p = MagicMock()
    mock_browser_context = MagicMock()
    mock_page = MagicMock()

    mock_sync_playwright.return_value.__enter__.return_value = mock_p
    mock_p.chromium.launch_persistent_context.return_value = mock_browser_context
    mock_browser_context.new_page.return_value = mock_page

    # Not a login page — URL is the target domain, no auth indicators
    mock_page.url = "https://example.com/dashboard"
    mock_page.evaluate.return_value = False
    mock_page.content.return_value = (
        "<html><body><h1>Dashboard</h1><p>Authorized user info</p></body></html>"
    )

    result = _fetch_authenticated_sync("https://example.com/dashboard")

    assert "# Dashboard" in result.content
    assert "Authorized user info" in result.content
    mock_browser_context.close.assert_called_once()


@patch("app.core.retriever.time")
@patch("app.core.retriever.sync_playwright")
def test_fetch_authenticated_sync_with_login_flow(mock_sync_playwright, mock_time):
    from app.core.retriever import _fetch_authenticated_sync

    mock_p = MagicMock()
    mock_browser_context = MagicMock()
    mock_page = MagicMock()

    mock_sync_playwright.return_value.__enter__.return_value = mock_p
    mock_p.chromium.launch_persistent_context.return_value = mock_browser_context
    mock_browser_context.new_page.return_value = mock_page

    # Initially lands on a login/auth page
    mock_page.evaluate.return_value = True
    mock_page.content.return_value = (
        "<html><body><h1>Protected Course</h1><p>Welcome student!</p></body></html>"
    )

    # Simulate: first poll still on auth page, second poll back on target
    mock_page.url = "https://app.joinhandshake.com/access?auth=true"
    url_sequence = [
        "https://app.joinhandshake.com/access?auth=true",  # 1st poll — still on auth
        "https://project-dynamo.learn.joinhandshake.com/introduction",  # 2nd poll — landed!
    ]
    type(mock_page).url = PropertyMock(
        side_effect=url_sequence
        + ["https://project-dynamo.learn.joinhandshake.com/introduction"] * 10
    )

    result = _fetch_authenticated_sync(
        "https://project-dynamo.learn.joinhandshake.com/introduction"
    )

    assert "# Protected Course" in result.content
    assert "Welcome student!" in result.content
    mock_browser_context.close.assert_called_once()


@patch("app.core.retriever.time")
@patch("app.core.retriever.sync_playwright")
def test_fetch_authenticated_sync_timeout_raises_error(mock_sync_playwright, mock_time):
    from app.core.retriever import _fetch_authenticated_sync

    mock_p = MagicMock()
    mock_browser_context = MagicMock()
    mock_page = MagicMock()

    mock_sync_playwright.return_value.__enter__.return_value = mock_p
    mock_p.chromium.launch_persistent_context.return_value = mock_browser_context
    mock_browser_context.new_page.return_value = mock_page

    # Stuck on auth page forever
    mock_page.evaluate.return_value = True
    mock_page.url = "https://app.joinhandshake.com/access?auth=true"

    with pytest.raises(RuntimeError, match="Authentication timed out"):
        _fetch_authenticated_sync(
            "https://project-dynamo.learn.joinhandshake.com/introduction"
        )

    mock_browser_context.close.assert_called_once()
