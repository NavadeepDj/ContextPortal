---
name: run-tests
description: >-
  Run and verify tests for the ContextPortal backend. Activate when running
  tests, adding new tests, debugging test failures, or verifying changes
  before declaring work complete. Covers the exact toolchain (uv + pytest),
  project conventions, and common pitfalls.
---

# Run Tests — ContextPortal Backend

## Quick Reference

### Run all tests
```powershell
cd backend
uv run pytest tests/ -v
```

### Run with coverage
```powershell
cd backend
uv run pytest tests/ -v --cov=app --cov-report=term-missing
```

### Run a single test file
```powershell
cd backend
uv run pytest tests/test_mcp.py -v
```

### Run a single test by name
```powershell
cd backend
uv run pytest tests/test_retriever.py -v -k "test_fetch_public_success"
```

### Run static analysis (ruff + mypy)
```powershell
cd backend
uv run ruff check app/ tests/
uv run mypy app/
```

---

## Project Test Conventions

### Toolchain
- **Package manager**: `uv` (NOT pip, NOT poetry)
- **Test runner**: `pytest` with `pytest-asyncio`
- **Async mode**: `asyncio_mode = "auto"` in `pyproject.toml` — all `async def test_*` functions are automatically collected as async tests. You do NOT need `@pytest.mark.asyncio` but the existing tests use it for explicitness.
- **Test directory**: `backend/tests/`
- **Configuration**: `backend/pyproject.toml`

### Test file naming
- `test_<module>.py` — maps to `app/<path>/<module>.py`
- Examples: `test_retriever.py` → `app/core/retriever.py`, `test_mcp.py` → `app/mcp/server.py`

### Existing test files
| File | Tests | What it covers |
|------|-------|----------------|
| `test_retriever.py` | 10 tests | `extract_markdown`, `fetch_public` (success, 401, 403, redirect, SPA shell, non-HTML, exception), `get_context` orchestration, `fetch_authenticated` thread delegation, Playwright login flow + timeout |
| `test_mcp.py` | 1 test (multi-assertion) | MCP tool registration, `fetch_context` tool call, security policy enforcement over MCP |
| `test_security.py` | Security policy tests | URL validation: scheme, localhost, private IPs |
| `test_api.py` | FastAPI endpoint tests | `/health`, `/c` endpoint |
| `test_health.py` | Health check tests | Basic health endpoint |

---

## Mocking Patterns

### Mock `httpx` for public fetch tests
```python
@patch("httpx.AsyncClient.get")
async def test_something(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.url = "https://example.com/page"
    mock_response.headers = {"content-type": "text/html; charset=utf-8"}
    mock_response.text = "<html>...</html>"
    mock_get.return_value = mock_response
```

### Mock `get_context` for MCP/API tests
```python
@pytest.fixture
def mock_get_context():
    with patch("app.mcp.server.get_context", new_callable=AsyncMock) as mock:
        mock.return_value = ContextResult(
            url="https://example.com",
            title="Title",
            content="# Content",
            retrieval_method="http",
            authenticated=False
        )
        yield mock
```

### Mock Playwright for authenticated tests
```python
@patch("app.core.retriever.sync_playwright")
def test_playwright_thing(mock_sync_playwright):
    mock_p = MagicMock()
    mock_browser_context = MagicMock()
    mock_page = MagicMock()
    mock_sync_playwright.return_value.__enter__.return_value = mock_p
    mock_p.chromium.launch_persistent_context.return_value = mock_browser_context
    mock_browser_context.new_page.return_value = mock_page
    # Set mock_page.url, mock_page.content(), mock_page.evaluate() as needed
```

### MCP in-memory test pattern
MCP tests use `create_client_server_memory_streams` for in-process testing:
```python
async with create_client_server_memory_streams() as (client_streams, server_streams):
    server = mcp._lowlevel_server
    # Start server task, create ClientSession, call tools
```

---

## Common Gotchas

1. **Always run from `backend/` directory** — `uv run pytest` resolves relative to the project root where `pyproject.toml` lives.
2. **Use `uv run`** — Do NOT activate a venv manually or use bare `pytest`. The project uses `uv` for dependency management.
3. **Playwright tests are sync** — `_fetch_authenticated_sync` uses `sync_playwright` (not async), run in a thread via `asyncio.to_thread`. Mock `sync_playwright`, not `async_playwright`.
4. **Mock `time.sleep`** — Playwright login poll tests mock `app.core.retriever.time` to avoid real waits.
5. **Security tests are negative tests** — Always test that blocked URLs return errors, not just that allowed URLs succeed.
6. **MCP server cleanup** — Always cancel the background server task in MCP tests to avoid hangs.

---

## What to Test for New Features

Per AGENT_RULES.md, every feature must have tests covering at minimum:
- ✅ Happy path
- ✅ Invalid input
- ✅ Expired state
- ✅ Revoked state
- ✅ Unauthorized access
- ✅ Malformed input
- ✅ Concurrent access (where applicable)
- ✅ Failure/retry behavior

Security-sensitive components require **negative tests** (verify that bad inputs are rejected).

---

## Pre-Commit Checklist

Before declaring work complete, run:
```powershell
cd backend
uv run pytest tests/ -v --cov=app --cov-report=term-missing
uv run ruff check app/ tests/
```

Both must pass with zero failures and zero lint errors.
