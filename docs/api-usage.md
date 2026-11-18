# FastAPI REST Endpoint Usage

ContextPortal is primarily designed to be consumed by AI agents via the Model Context Protocol (MCP) CLI. However, the core retrieval engine is also exposed via a standard HTTP REST API using FastAPI.

## Starting the API Server

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --no-access-log
```

Disable access logging to keep the target URL out of Uvicorn's logs. The target is passed in the request query string, so apply the same rule to any reverse proxy that logs requests to `/c`.

## Retrieving Context

You can request any URL through the `/c` endpoint:

```
GET http://localhost:8000/c?url=https://example.com/some-protected-page
```

### Behavior:
- **Public pages** are fetched instantly via HTTP and returned as Markdown.
- **Protected pages** trigger a Playwright browser window where you log in manually (if a session doesn't already exist). Once authenticated, the content is extracted and returned as clean Markdown.
- **Sign-in required or session expired** returns HTTP 401 with `detail.code` set to `authentication_required`.
- **Access denied by the target site** returns HTTP 403 with `detail.code` set to `access_denied`.

The API reuses the browser profile at `~/.contextportal/playwright_profile`.

