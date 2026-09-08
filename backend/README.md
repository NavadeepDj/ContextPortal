# 🔑 ContextPortal

> **Give your AI agent access to authenticated web pages — without giving it your credentials.**

Your AI agent can fetch any public webpage. But the moment it hits a login wall — Jira, Confluence, internal wikis, enterprise dashboards — it's stuck.

ContextPortal sits between your AI agent and the web. When the agent needs a protected page, ContextPortal uses *your* existing browser session to grab it, strips out all the noise, and hands back clean Markdown. The agent gets context. It never gets your cookies.

> 🤖 **Agent:** *"I can't read this ticket. It's behind an SSO login wall. Please take 5 screenshots."*  
> 👤 **You:** *"No way. Why am I doing homework for an AI?"*  
> 🔑 **ContextPortal:** *"Say less. Log in once in your browser; your agent retrieves the page forever."*

### 🏛️ The 4 Pillars
- 🛑 **Stop feeding your AI screenshots.** Copy-paste is not an agent architecture.
- 🔁 **Authenticate once. Retrieve context continuously.** Log in once; your agent reads forever.
- 🔐 **Your browser holds the session. Your agent gets the page. Zero cookies leaked.**
- 🎯 **Give your agent a retrieval tool, not a browser to operate.** Clean Markdown, zero DOM fragility.

## 🔌 Connect ContextPortal to your AI

ContextPortal works through the Model Context Protocol (MCP) and configures supported AI clients automatically.

```text
┌──────────────────────────────────────────────┐
│  Connect your agent                          │
│                                              │
│  $ contextportal setup                       │
│                                              │
│  ✓ MCP server                                │
│  ✓ Browser profile                           │
│  ✓ AI client                                 │
│                                              │
│  Ready.                                      │
└──────────────────────────────────────────────┘
```

Onboarding shouldn't feel like wrestling with JSON files and virtual environments.  
It's three steps: **Install ContextPortal → Connect your agent → Give it the URL.**

---

### Step 1: Install ContextPortal

```bash
uv tool install contextportal
```

---

### Step 2: Connect your AI agent

```bash
contextportal setup
```

That's it! ContextPortal scans your system, detects installed AI agent clients, creates a safety backup, and registers the MCP server automatically.

> 🩺 Run `contextportal doctor` anytime to audit your system health and client connections.

---

### 🤖 Supported AI Clients

ContextPortal provides zero-friction automatic setup for major AI developer tools, plus a standard manual fallback:

| AI Client | Platform | Automatic Setup | Manual Config Path |
| :--- | :--- | :--- | :--- |
| **Cursor** | Win / Mac / Linux | `contextportal setup --client cursor` | `~/.cursor/mcp.json` |
| **Google Antigravity** | Win / Mac / Linux | `contextportal setup --client antigravity` | `~/.gemini/antigravity/mcp_config.json` |
| **Claude Desktop** | Win / Mac / Linux | `contextportal setup --client claude` | `%APPDATA%\Claude\` or `~/Library/Application Support/Claude/` |
| **VS Code (Cline / Roo / Copilot)** | Universal | Built-in MCP settings | `.vscode/mcp.json` or Extension settings |
| **Any Custom MCP Client** | Universal | STDIO transport | Standard JSON payload |

---

### Step 3: Log into your private sites (once)

```bash
contextportal login
```

A clean browser opens. Log into your private tools — Jira, Confluence, internal wikis, GitHub enterprise, Handshake. Close the window when you're done. Your session stays locally on your machine.

---

### 🎉 You're ready. Now just give your agent the URL.

In your AI chat (Cursor, Claude, Antigravity, etc.):

> *"Summarize the roadmap at https://internal.company.com/q3-roadmap"*

Your agent calls ContextPortal → ContextPortal retrieves the page through your authenticated session → clean, token-optimized Markdown comes back.

**No screenshots. No copy-pasting. You're done.**

---

### 🛠️ Manual Configuration Fallback (Optional)

If you prefer to configure manually:

```json
{
  "mcpServers": {
    "context-portal": {
      "command": "contextportal",
      "args": ["mcp"]
    }
  }
}
```

Works with **Cursor**, **Claude Desktop**, **Antigravity**, **VS Code**, and any MCP client.

## Learn More

- 📖 [Full Documentation](https://github.com/NavadeepDj/ContextPortal)
- 🔐 [Security Model](https://github.com/NavadeepDj/ContextPortal/blob/main/docs/security-and-automation-philosophy.md)
- 🗺️ [Product Roadmap](https://github.com/NavadeepDj/ContextPortal/blob/main/PRODUCT_ROADMAP.md)
