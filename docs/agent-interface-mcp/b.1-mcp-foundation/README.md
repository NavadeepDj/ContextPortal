# Phase B.1: MCP Foundation

## The Goal
The core purpose of ContextPortal is to fetch authenticated content from the web. However, to be useful to an AI agent (like Cursor, Claude Desktop, or Antigravity), ContextPortal needs a standardized way to communicate. 

We use the **Model Context Protocol (MCP)** for this. MCP is an open standard that allows AI agents to discover and execute tools securely. Phase B.1 establishes this foundational communication layer.

## Architectural Rule
A critical design principle of ContextPortal is separation of concerns:
- **The MCP Layer** knows *how to talk to the AI*.
- **The Retrieval Engine** knows *how to talk to the web*.

The MCP server must **never** contain browser automation logic or session management. It strictly acts as a translator between the agent and the underlying python retrieval service.

## Implementation Details

### Dependency Selection
We chose the **official v2 Model Context Protocol Python SDK** (`mcp[cli]`). 
*Why?* The ecosystem has evolved rapidly. Older tutorials often recommend third-party libraries (like `fastmcp`), but the official SDK has recently absorbed these high-level APIs directly into `mcp.server.mcpserver`. By using the official v2 SDK, we ensure maximum compatibility and long-term support.

### The Server API
The server is initialized in `backend/app/mcp/server.py`. 

```python
from mcp.server.mcpserver import MCPServer
mcp = MCPServer("ContextPortal")
```

We defined our first tool, `fetch_context(url: str)`. In this foundational phase, the tool intentionally does *nothing* except return a success string (`"MCP connection successful"`). This isolation proves that the agent can connect to the server without worrying about web scraping bugs.

### How We Tested It (In-Memory Streams)
Testing an MCP server usually requires launching it as a separate background process and communicating over standard input/output (STDIO) pipes. This can be flaky and slow.

Instead, we used the official SDK's **in-memory testing utility**:
```python
from mcp.shared.memory import create_client_server_memory_streams
```
This allowed us to wire a virtual MCP Client directly to our MCP Server entirely within Python memory. The test successfully proved that:
1. An agent can connect.
2. The agent can ask for a list of available tools (`session.list_tools()`).
3. The agent can execute the `fetch_context` tool and receive the expected text.

