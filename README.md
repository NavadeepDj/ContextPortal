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
