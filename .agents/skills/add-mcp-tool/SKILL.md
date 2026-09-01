---
name: add-mcp-tool
description: >-
  Add a new MCP tool to the ContextPortal MCP server. Activate when
  creating a new agent-facing capability, extending the MCP server,
  or adding a new tool that agents can call. Covers the registration
  pattern, security enforcement, response formatting, error handling,
  and testing with the in-memory MCP test harness.
---

# Add MCP Tool — ContextPortal

## Architecture Overview

ContextPortal exposes capabilities to AI agents via an MCP (Model Context Protocol) server.

```
Agent (Claude, Gemini, etc.)
    ↓ MCP protocol (STDIO transport)
app/mcp/server.py  ← MCP tool definitions
    ↓
app/core/*          ← Business logic (retriever, security, etc.)
```

**Key files**:
- MCP server: `backend/app/mcp/server.py`
- MCP tests: `backend/tests/test_mcp.py`
- Security policy: `backend/app/core/security.py`
- Core logic: `backend/app/core/`

---

## Step-by-Step: Adding a New Tool

### Step 1: Implement the core logic

Create or extend a module in `backend/app/core/`. The MCP tool should be a thin wrapper that delegates to core logic.

**DO NOT** put business logic directly in the tool function.

```python
# backend/app/core/my_feature.py
from pydantic import BaseModel

class MyResult(BaseModel):
    """Typed result model for the feature."""
    data: str
    status: str

async def do_my_feature(param: str) -> MyResult:
    """Core business logic, fully testable independently."""
    # ... implementation
    return MyResult(data="...", status="ok")
```

### Step 2: Register the MCP tool

Add the tool in `backend/app/mcp/server.py`:

```python
from app.core.security import validate_url_policy  # if URL is involved
from app.core.my_feature import do_my_feature

@mcp.tool()
async def my_tool_name(param: str) -> str:
    """Clear, agent-readable docstring explaining what this tool does.
    This docstring is what the agent sees when it discovers the tool.
    """
    # 1. Input validation
    if not param:
        raise ValueError("param is required")

    # 2. Security policy (if URL is involved)
    try:
        validate_url_policy(param)
    except ValueError as e:
        return f"Error: {str(e)}"

    # 3. Delegate to core logic
    try:
        result = await do_my_feature(param)
        # 4. Format response as agent-readable text
        return f"# Result\n**Status**: {result.status}\n\n{result.data}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### Step 3: Update the tool count in tests

In `backend/tests/test_mcp.py`, update the tool count assertion:

```python
# Before (1 tool):
assert len(tools_response.tools) == 1

# After (2 tools):
assert len(tools_response.tools) == 2
```

### Step 4: Add tests for the new tool

Add test cases in `backend/tests/test_mcp.py` using the in-memory MCP harness:

```python
@pytest.mark.asyncio
async def test_mcp_my_tool_name(mock_my_feature):
    async with create_client_server_memory_streams() as (client_streams, server_streams):
        server = mcp._lowlevel_server

        init_options = InitializationOptions(
            server_name="ContextPortal",
            server_version="0.1.0",
            capabilities=server.get_capabilities(
                notification_options=None,
                experimental_capabilities={}
            )
        )

        server_task = asyncio.create_task(
            server.run(server_streams[0], server_streams[1], init_options)
        )

        try:
            async with ClientSession(client_streams[0], client_streams[1]) as session:
                await session.initialize()

                # Happy path
                result = await session.call_tool("my_tool_name", {"param": "test"})
                assert not result.is_error
                assert "Expected content" in result.content[0].text

                # Security enforcement (if URL-based)
                result_bad = await session.call_tool("my_tool_name", {"param": "http://localhost"})
                assert "Error:" in result_bad.content[0].text

                # Invalid input
                result_empty = await session.call_tool("my_tool_name", {"param": ""})
                # Verify appropriate error handling
        finally:
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass
```

### Step 5: Run tests and verify

```powershell
cd backend
uv run pytest tests/test_mcp.py -v
uv run pytest tests/ -v  # full suite
```

---

## Design Rules

### Tool Naming
- Use `snake_case` for tool names
- Names should be verb-noun: `fetch_context`, `list_sources`, `revoke_token`
- The name is what agents see and call — make it descriptive

### Docstrings
- The tool docstring is the agent's only documentation for the tool
- Be specific about what it does, what parameters it accepts, and what it returns
- Include any limitations or prerequisites

### Error Handling Pattern
ContextPortal returns errors as formatted strings (not exceptions) so the agent can understand what went wrong:

```python
# ✅ Correct — agent can read and react
return f"Error: {str(e)}"

# ❌ Wrong — agent gets an opaque MCP error
raise Exception(str(e))
```

### Security Enforcement
- If the tool accepts a URL, **always** call `validate_url_policy()` before any fetch
- If the tool accesses user-scoped data, **always** verify authorization
- Never expose credentials, tokens, or internal paths in responses

### Response Formatting
Format responses as **Markdown** that agents can easily parse:
```python
formatted = (
    f"# {result.title}\n"
    f"**Source URL**: {result.url}\n"
    f"**Status**: {result.status}\n"
    f"---\n\n"
    f"{result.content}"
)
```

---

## Checklist

```markdown
- [ ] Core logic in `app/core/`, NOT in the tool function
- [ ] Tool registered with `@mcp.tool()` in `app/mcp/server.py`
- [ ] Clear agent-readable docstring
- [ ] Input validation
- [ ] Security policy enforcement (if URL-based)
- [ ] Errors returned as strings, not exceptions
- [ ] Response formatted as Markdown
- [ ] Tool count updated in `test_mcp.py`
- [ ] Happy path test
- [ ] Security enforcement test
- [ ] Invalid input test
- [ ] All tests pass: `uv run pytest tests/ -v`
```
