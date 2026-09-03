# 🔑 ContextPortal

> **Give your AI agent access to authenticated web pages — without giving it your credentials.**

Your AI agent can fetch any public webpage. But the moment it hits a login wall — Jira, Confluence, internal wikis, enterprise dashboards — it's stuck.

ContextPortal sits between your AI agent and the web. When the agent needs a protected page, ContextPortal uses *your* existing browser session to grab it, strips out all the noise, and hands back clean Markdown. The agent gets context. It never gets your cookies.

> 🍪 *Agent: "Can I have your cookies?"*  
> 🚫 *ContextPortal: "No. Here's the page."*

## Install

```bash
uv tool install contextportal
```

## Setup

```bash
# Log into your private sites (once)
contextportal login

# Test it
contextportal fetch https://your-protected-site.com/docs
```

## Connect to your AI Agent

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

Works with **Cursor**, **Claude Desktop**, **Antigravity**, **VS Code**, and any MCP-compatible client.

## Learn More

- 📖 [Full Documentation](https://github.com/NavadeepDj/ContextPortal)
- 🔐 [Security Model](https://github.com/NavadeepDj/ContextPortal/blob/main/docs/security-and-automation-philosophy.md)
- 🗺️ [Product Roadmap](https://github.com/NavadeepDj/ContextPortal/blob/main/PRODUCT_ROADMAP.md)
