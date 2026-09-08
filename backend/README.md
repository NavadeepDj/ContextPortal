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

## Install

```bash
uv tool install contextportal
```

## 🪄 Quick Setup (Auto-Config)

Configure your AI agent (Claude Desktop, Cursor, Antigravity) with a single command:

```bash
contextportal setup
```

Verify your environment anytime:

```bash
contextportal doctor
```

## 🔐 Log In (Once)

Log into your private sites in your local browser — your session is saved automatically:

```bash
contextportal login
```

Test it directly:

```bash
contextportal fetch https://your-protected-site.com/docs
```

## 🔌 Manual MCP Configuration (Optional)

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
