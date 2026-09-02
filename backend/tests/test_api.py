import pytest
from unittest.mock import patch
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.retriever import ContextResult


@pytest.mark.asyncio
@patch("app.main.get_context")
async def test_fetch_context_endpoint_success(mock_get_context):
    mock_get_context.return_value = ContextResult(
        url="https://example.com/article",
        title="Extracted Article Content",
        content="# Extracted Article Content\n\nThis is sample markdown.",
        retrieval_method="http",
        authenticated=False,
    )
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/c?url=https://example.com/article")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert response.text == "# Extracted Article Content\n\nThis is sample markdown."
    mock_get_context.assert_called_once_with("https://example.com/article")


@pytest.mark.asyncio
async def test_fetch_context_endpoint_invalid_url():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/c?url=not-a-valid-url")

    assert response.status_code == 422


@pytest.mark.asyncio
@patch("app.main.get_context")
async def test_fetch_context_endpoint_error(mock_get_context):
    mock_get_context.side_effect = Exception("Retrieval failed")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/c?url=https://example.com/fails")

    assert response.status_code == 500
    assert response.json()["detail"] == "Retrieval failed"
