# Phase B.3: Retrieval Orchestrator

## Objective
Connect the foundational MCP tool layer (Phase B.1) and the Security boundary (Phase B.2) to the actual content retrieval engine built in Phase A.

## Architectural Decision: Strict Decoupling
The primary rule of this phase is that the MCP layer remains completely ignorant of *how* the retrieval happens. 

In `backend/app/mcp/server.py`, the `fetch_context` tool simply calls:
```python
content = await get_context(url)
```

It does not know if:
- `httpx` was used for a fast public HTTP fetch.
- `Playwright` was used to launch a visible Chrome browser.
- A user had to log in interactively via an OAuth popup.
- The authentication session was loaded from a persistent browser profile.

This decoupled design means we can completely rewrite the underlying browser automation engine (e.g., swapping Playwright for Selenium, or updating how cookies are stored) without ever touching the MCP layer or breaking AI agents.

## Error Handling
If `get_context(url)` returns `None` (for example, if a page is entirely blank or auth failed unexpectedly), the MCP tool intercepts this and returns a verbose error string:
```text
"Error: Could not retrieve content from the URL. The page might be empty, heavily obfuscated, or the auth session may have expired."
```
As with Phase B.2, returning descriptive strings prevents agents from getting stuck in "UnexpectedToolError" retry loops.

## Testing Strategy
To maintain the speed of the MCP in-memory tests, we use `unittest.mock.AsyncMock` to patch `get_context`. This ensures our protocol tests verify the orchestrator handoff successfully without accidentally spinning up a real headless browser during CI runs.

