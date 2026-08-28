# Phase B.5: Real Agent Integration

## Objective
The final milestone of Phase B is connecting a real-world AI agent to ContextPortal. With the MCP Server completed, secured, and returning structured data, it is now ready to be consumed by agents like **Claude Desktop**, **Cursor**, or **Antigravity**.

Because we built ContextPortal using the official standard Model Context Protocol over STDIO, integrating it requires **zero custom code** on the agent side. It is entirely configuration-driven.

---

## 🚀 How to Connect Your Agent

At the root of this repository, you will find `mcp_config.example.json`. 

```json
{
  "mcpServers": {
    "context-portal": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "-m",
        "app.mcp.server"
      ],
      "cwd": "<ABSOLUTE_PATH_TO_YOUR_PROJECT>/backend"
    }
  }
}
```

### 1. Claude Desktop Integration
Claude Desktop natively reads a configuration file to spawn local MCP servers.
1. Open the Claude Desktop configuration file:
   - **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
2. Copy the contents of `mcp_config.example.json` into this file.
3. Replace `<ABSOLUTE_PATH_TO_YOUR_PROJECT>` with the actual path to the cloned repository.
4. Restart Claude Desktop. You will now see a **⚒️ 1 Tool** icon indicating that Claude has discovered the `fetch_context` tool!

### 2. Cursor IDE Integration
Cursor allows you to add MCP servers directly through its settings UI.
1. Open Cursor Settings > **Features** > **MCP Servers**.
2. Click **+ Add new MCP server**.
3. **Name**: `context-portal`
4. **Type**: `command`
5. **Command**: `uv run python -m app.mcp.server`
6. Make sure to set the execution directory (cwd) to the `backend/` folder of this project.

### 3. Google Antigravity Integration
Antigravity supports MCP natively via its plugin ecosystem.
You can configure it via the MCP JSON configuration or by registering the command line execution directly into the Antigravity server registry.

---

## What the Agent Sees
Once connected, the agent will have access to the following tool signature:

```typescript
function fetch_context(url: string): string
```

When the agent executes it, it receives the highly readable, structured Markdown document designed in Phase B.4 (including the Title, URL, and Authentication status), allowing it to read paywalled articles, private repositories, and internal enterprise dashboards seamlessly.
