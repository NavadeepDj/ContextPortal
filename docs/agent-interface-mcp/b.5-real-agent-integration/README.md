# Phase B.5: Real Agent Integration & Live Verification

## Objective
The final milestone of Phase B is connecting a real-world AI agent to ContextPortal and proving the core thesis end-to-end:
> **An AI agent requests a URL over standard MCP. If public, ContextPortal retrieves it over HTTP. If protected, ContextPortal leverages the user's authorized browser session to extract clean Markdown context with zero credential leakage.**

Because ContextPortal implements the official Model Context Protocol over standard STDIO, integrating it requires **zero custom code** on the agent side.

---

## 🚀 Agent Configuration Setup

### 1. Google Antigravity Integration (Verified)
Antigravity reads active user MCP servers from its global configuration:
* **Config File**: `~/.gemini/config/mcp_config.json` (on Windows: `C:\Users\<username>\.gemini\config\mcp_config.json`)
* **Workspace Config**: `.agents/mcp_config.json`

```json
{
  "mcpServers": {
    "context-portal": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "C:\\Users\\<username>\\ContextPortal\\backend",
        "python",
        "-m",
        "app.mcp.server"
      ]
    }
  }
}
```

### 2. Claude Desktop Integration
Add the configuration to `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS).

### 3. Cursor IDE Integration
In Cursor Settings ➔ **Features** ➔ **MCP Servers**, add `context-portal` with command `uv run --directory <path-to-backend> python -m app.mcp.server`.

---

## 🧪 Live End-to-End Verification Results

We verified ContextPortal live with the **Antigravity AI Agent** using the registered `fetch_context` tool.

### Test Case 1: Public Web Page
* **Tool Invocation**: `fetch_context(url="https://example.com")`
* **Execution Path**: Agent ➔ MCP Server ➔ `fetch_public` (`httpx`) ➔ Readability Markdown
* **Result**:
  ```markdown
  # Example Domain
  **Source URL**: https://example.com
  **Retrieval Method**: http (Authenticated: False)
  ---
  # Example Domain
  This domain is for use in documentation examples without needing permission...
  ```

### Test Case 2: Protected Enterprise Portal (Handshake Project Dynamo)
* **Tool Invocation**: `fetch_context(url="https://project-dynamo.learn.joinhandshake.com/introduction")`
* **Execution Path**: 
  1. Agent passes URL to `fetch_context`.
  2. Public fetch redirected/blocked.
  3. `fetch_authenticated` spawns Playwright with persistent user profile (`./playwright_profile`).
  4. Session detected and authenticated.
  5. HTML extracted and converted to clean structured Markdown.
* **Result**:
  ```markdown
  # Lovable App
  **Source URL**: https://project-dynamo.learn.joinhandshake.com/introduction
  **Retrieval Method**: browser (Authenticated: True)
  ---
  ## What a task is
  A task is a self-contained challenge that runs inside a Docker container. You author a few things...
  ## Harbor
  Harbor is the CLI you'll use throughout...
  ```

---

## 🛡️ Security & Privacy Summary
- **Zero Credential Leakage**: No cookies, session storage tokens, or local file paths were serialized or exposed to the agent.
- **SSRF Hardening**: Non-HTTP schemes (`file://`) and internal IP ranges (`localhost`, `127.0.0.1`, RFC 1918) are rejected before retrieval.
- **Transparent Automation**: The user remains in control of authentication while the agent receives structured, clean Markdown context.
