---
name: configure-mcp-client
description: >-
  Configure AI agent clients (Antigravity IDE, Claude Desktop, Cursor) to connect
  to the ContextPortal MCP server over STDIO. Activate when setting up or troubleshooting
  MCP integration for an agent, configuring mcp_config.json, or verifying live tool connections.
---

# Configure MCP Client — ContextPortal

## Overview

ContextPortal exposes its capabilities via the Model Context Protocol (MCP) using a standard **STDIO transport**.
Any compatible AI agent can connect to it by executing Python within the project's `backend` virtual environment using `uv`.

**Server Command**:
```powershell
uv run --directory <PATH_TO_PROJECT>/backend python -m app.mcp.server
```

---

## 1. Antigravity IDE Configuration

Antigravity loads active MCP servers from its global configuration file, with fallback/project declarations in workspace `.agents/`.

### Configuration Files
- **Global (Active in IDE)**: `~/.gemini/config/mcp_config.json` (Windows: `C:\Users\<username>\.gemini\config\mcp_config.json`)
- **Workspace (Checked into Repo)**: `.agents/mcp_config.json`

### JSON Schema
```json
{
  "mcpServers": {
    "context-portal": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "<ABSOLUTE_PATH_TO_PROJECT>\\backend",
        "python",
        "-m",
        "app.mcp.server"
      ]
    }
  }
}
```

> [!IMPORTANT]
> Always use `--directory <path>\backend` instead of relying purely on `cwd` to prevent working-directory resolution issues on Windows.

---

## 2. Claude Desktop Configuration

Claude Desktop discovers local STDIO servers from its desktop config:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "context-portal": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "<ABSOLUTE_PATH_TO_PROJECT>/backend",
        "python",
        "-m",
        "app.mcp.server"
      ]
    }
  }
}
```

---

## 3. Cursor IDE Configuration

1. Open Cursor Settings (`Ctrl+,` or `Cmd+,`).
2. Navigate to **Features** ➔ **MCP Servers** ➔ click **+ Add new MCP server**.
3. Fill in:
   - **Name**: `context-portal`
   - **Type**: `command`
   - **Command**: `uv run --directory <ABSOLUTE_PATH_TO_PROJECT>\backend python -m app.mcp.server`

---

## 4. Verification & Testing Procedure

Once configured, verify the connection in order:

### Step 1: Check UI Connection Status
In Antigravity IDE:
1. Open the Chat / Agent panel.
2. Click **`...` (More Options)** in the top right.
3. Select **MCP Servers**.
4. Confirm `context-portal` is ● **Connected** with tool `fetch_context`.

### Step 2: Public URL Smoke Test
Ask the agent:
> *"Use the `fetch_context` MCP tool to retrieve `https://example.com` and show me the extracted content."*

Expected result:
- Formatted markdown header with title `# Example Domain`.
- `**Retrieval Method**: http (Authenticated: False)`.

### Step 3: Authenticated Retrieval Test
Ask the agent to retrieve a protected resource (e.g. Handshake portal):
> *"Use the `fetch_context` MCP tool to retrieve `https://project-dynamo.learn.joinhandshake.com/introduction`."*

Expected result:
- Browser session loads in transparent mode.
- Context extracted and returned with `**Retrieval Method**: browser (Authenticated: True)`.

---

## Common Troubleshooting & Gotchas

1. **Server not found / 0 tools discovered**:
   - Verify `~/.gemini/config/mcp_config.json` is not empty.
   - Check path for typos (e.g., hardcoded usernames from other machines).
2. **`uv` not recognized in agent environment**:
   - Ensure `uv` is in system `PATH`, or specify full path to `uv.exe` in `"command"`.
3. **STDIO hangs or crashes immediately**:
   - Test manually in terminal: `cd backend; uv run python -m app.mcp.server`. If it sits waiting for input, the server is healthy. If it exits with a Python traceback, fix the traceback first.

