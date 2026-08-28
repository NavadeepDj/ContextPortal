# ContextPortal

> The authenticated fetch layer for AI agents.

Give an agent a URL. If it's public, fetch it normally. If it's protected, use the user's legitimate authorized session. Return clean, agent-readable context.

## Quick Start (MVP)

```bash
cd backend
uv sync
uv run playwright install chromium
uv run uvicorn app.main:app --reload
```

Then request any URL through ContextPortal:

```
http://localhost:8000/c?url=https://example.com/some-protected-page
```

- **Public pages** are fetched instantly via HTTP.
- **Protected pages** trigger a Playwright browser window where you log in manually. Once authenticated, the content is extracted and returned as clean Markdown.

## How It Works

```
Agent (or browser)
  ↓
GET /c?url=<target>
  ↓
ContextPortal
  ↓
┌─────────────────┐
│ Public?          │──→ Normal HTTP fetch → Markdown → Return
│ Protected?       │──→ Playwright browser (user logs in) → Extract → Markdown → Return
└─────────────────┘
```

The browser is an implementation detail. The URL is the interface.

## Project Documentation

| File | Purpose |
|---|---|
| **[`docs/PRODUCT_THESIS.md`](docs/PRODUCT_THESIS.md)** | Core product definition — read this first |
| **[`AGENT_RULES.md`](AGENT_RULES.md)** | Security and engineering rules for AI agents |
| **[`AGENTS.md`](AGENTS.md)** | Agent entry point & OpenWiki pointer |
| **[`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md)** | Current phase and next steps |
| **[`decisions/`](decisions/)** | Architecture Decision Records |
| **[`docs/`](docs/)** | Human-maintained documentation |
| **[`openwiki/`](openwiki/quickstart.md)** | Automated living codebase evidence index |

## Development Phases

- [x] **Phase 0** — Repository bootstrap (FastAPI, uv, Next.js scaffold)
- [x] **Phase A** — Retrieval Proof (current MVP)
- [ ] **Phase B** — Agent Interface (MCP or similar)
- [ ] **Phase C** — Resource Isolation
- [ ] **Phase D** — Authentication Session Management
- [ ] **Phase E** — Security Hardening
- [ ] **Phase F** — Production Infrastructure
