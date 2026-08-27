# ContextPortal

Context behind the login? Just send the link.

ContextPortal is an authenticated context proxy that securely turns authenticated web pages, private APIs, and enterprise data into agent-ready context.

## Development Setup

1. Start Redis infrastructure:
   ```bash
   docker compose up -d
   ```

2. Start the FastAPI Backend:
   ```bash
   cd backend
   uv sync
   uv run uvicorn app.main:app --reload
   ```

3. Start the Next.js Frontend:
   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```

## Agent Documentation & Instructions

ContextPortal uses a layered agent instruction and documentation setup:

| File | Purpose |
|---|---|
| **[`AGENT_RULES.md`](AGENT_RULES.md)** | Core security and engineering rules (ephemeral proxy, SSRF, token security) |
| **[`AGENTS.md`](AGENTS.md)** | Root agent entry point & OpenWiki index pointer |
| **[`CLAUDE.md`](CLAUDE.md)** | Compatibility forwarder to `AGENTS.md` for Claude Code CLI |
| **[`docs/`](docs/agent-architecture-and-rules.md)** | Human-maintained project & architecture documentation |
| **[`openwiki/`](openwiki/quickstart.md)** | Automated living codebase evidence index |

### OpenWiki Commands
- **Update Wiki**: `openwiki --update`
- **Configure Gemini Provider**:
  ```powershell
  $env:OPENWIKI_PROVIDER="gemini"
  $env:GEMINI_API_KEY="your-api-key"
  openwiki --update --modelId gemini-2.5-flash
  ```
- **Interactive Visualizer**: `openwiki visualize`


