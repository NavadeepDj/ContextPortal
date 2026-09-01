# ContextPortal

> The authenticated fetch layer for AI agents.

Give an AI agent a URL. 

- **Public?** → Fetch normally.
- **Protected?** → Use your authorized browser session.

ContextPortal ensures your agent gets the clean Markdown content it needs, without ever granting the agent access to your browser, your passwords, or your cookies.

*Agent: "Can I have your cookies?"*
*ContextPortal: "No. Here is the page."*

---

## 🚀 The "First 5 Minutes" Quickstart

### 1. Install

```bash
# Clone the repository
git clone https://github.com/NavadeepDj/ContextPortal.git
cd ContextPortal/backend

# Install the ContextPortal CLI and dependencies
uv pip install -e .
uv run playwright install chromium
```

### 2. Authenticate (Pre-warm your session)

You only need to do this once per private website (like Jira, Handshake, internal wikis, etc.).

```bash
uv run contextportal login
```
*A secure Chrome window will open. Log into your private sites normally, then close the window. Your session is securely saved locally.*

### 3. Connect to your AI Agent

Add ContextPortal to your AI agent's MCP configuration (Cursor, Claude Desktop, Antigravity, etc.):

```json
{
  "mcpServers": {
    "contextportal": {
      "command": "uv",
      "args": [
        "run", 
        "--directory", 
        "/absolute/path/to/ContextPortal/backend", 
        "contextportal", 
        "mcp"
      ]
    }
  }
}
```

### 4. Fetch

Ask your AI agent:
> *"Fetch the requirements from https://project-dynamo.learn.joinhandshake.com/introduction"*

ContextPortal will seamlessly route the request, utilize your local authenticated session, extract the content, and hand the agent clean Markdown. 

Done.

---

## 🏗️ Architecture & Philosophy

The agent shouldn't need to know *how* a page is retrieved. It just conceptually calls `fetch(url)`. ContextPortal handles the complex tiering invisibly:

1. **Fast HTTP**: For public Wikipedia, blogs, and static sites.
2. **Persistent Browser Session**: For protected enterprise portals, automatically using the local session you established via `contextportal login`.

By keeping the ContextPortal Gateway **local**, your credentials never leave your machine, and your agent only receives the context it specifically asked for.

---

## 📚 Documentation

| File | Purpose |
|---|---|
| **[`docs/PRODUCT_THESIS.md`](docs/PRODUCT_THESIS.md)** | Core product definition & architecture — read this first |
| **[`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md)** | Current development phase and roadmap |
| **[`AGENT_RULES.md`](AGENT_RULES.md)** | Security and engineering rules for AI agents |
| **[`docs/api-usage.md`](docs/api-usage.md)** | Instructions for using the FastAPI REST endpoint |
| **[`decisions/`](decisions/)** | Architecture Decision Records (ADRs) |
| **[`openwiki/`](openwiki/quickstart.md)** | Automated living codebase evidence index |
