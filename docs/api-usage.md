# FastAPI REST Endpoint Usage

ContextPortal is primarily designed to be consumed by AI agents via the Model Context Protocol (MCP) CLI. However, the core retrieval engine is also exposed via a standard HTTP REST API using FastAPI.

## Starting the API Server

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

## Retrieving Context

You can request any URL through the `/c` endpoint:

```
GET http://localhost:8000/c?url=https://example.com/some-protected-page
```

### Behavior:
- **Public pages** are fetched instantly via HTTP and returned as Markdown.
- **Protected pages** trigger a Playwright browser window where you log in manually (if a session doesn't already exist). Once authenticated, the content is extracted and returned as clean Markdown.

*Note: This API is stateless and relies on the local `./playwright_profile` directory for browser session persistence.*

