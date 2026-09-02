# Building the ContextPortal Python Package

## 1. Overview & Architecture

ContextPortal is designed as an authenticated fetch layer for AI agents. While it started as an internal script executed via direct module paths (`python -m app.mcp.server`), Phase C transforms it into a standardized, installable Python CLI package.

Packaging the backend allows:
- **Zero-knowledge installation**: Any developer or agent can install it globally using `uv tool install` or `pip install`.
- **Trivial Agent Configuration**: MCP client configs (in Cursor, Claude Desktop, Antigravity) no longer require hardcoding local repository filepaths or virtualenv script interpreters. They simply call `contextportal mcp`.
- **Unified CLI Capabilities**: Exposes `mcp`, `login`, and `fetch` subcommands for both agents and human users.

---

## 2. Package Configuration (`pyproject.toml`)

The package metadata and build backend are defined in `backend/pyproject.toml`.

```toml
[project]
name = "contextportal-backend"
version = "0.1.0"
description = "ContextPortal — Authenticated context proxy for AI agents"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "redis[hiredis]>=5.0.0",
    "pydantic-settings>=2.4.0",
    "httpx>=0.27.0",
    "playwright>=1.62.0",
    "readability-lxml>=0.8.4.1",
    "markdownify>=1.2.3",
    "mcp[cli]>=2.1.1",
]

[project.scripts]
contextportal = "app.cli:main"

[tool.setuptools.packages.find]
where = ["."]
include = ["app", "app.*"]
```

---

## 3. Critical Packaging Pitfalls & Solutions

During the Phase C build process, we encountered two subtle but critical packaging pitfalls:

### Pitfall 1: Flat-Layout Auto-Discovery with Runtime Folders
**The Problem:**
By default, `setuptools` scans the root directory for any subdirectories to package. When ContextPortal runs, Playwright creates a `playwright_profile/` directory containing cookies, IndexedDB records, and local storage. Setuptools identified both `app` and `playwright_profile` as top-level Python modules, failing the build with:
```text
error: Multiple top-level packages discovered in a flat-layout: ['app', 'playwright_profile'].
```
*Security Risk:* If setuptools had not failed, it would have bundled the user's private cookies into the distributed wheel artifact.

### Pitfall 2: Naive `packages = ["app"]` Breaking Subpackages
**The Problem:**
To fix Pitfall 1, we initially added:
```toml
[tool.setuptools]
packages = ["app"]
```
While this resolved the build error, it instructed setuptools to bundle **only** the top-level `app/` folder (`__init__.py` and `cli.py`), completely omitting `app/core/` (`retriever.py`, `security.py`) and `app/mcp/` (`server.py`). 

When executed, the CLI immediately crashed with:
```text
ModuleNotFoundError: No module named 'app.core'
```

### The Permanent Solution: Explicit Recursive Package Find
We configured `setuptools.packages.find` with an explicit glob pattern that includes all nested submodules while ignoring all other top-level folders:
```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["app", "app.*"]
```

---

## 4. Avoiding Relative Paths for CLI State

When ContextPortal runs as an installed global binary, the user's Current Working Directory (`CWD`) changes constantly. 

**Rule:** Never use `./` relative paths for state, profiles, or caches.

```python
# ❌ Buggy: State is fragmented across every directory the user runs the tool from
profile_dir = Path("./playwright_profile")

# ✅ Correct: State is globally unified and deterministic across all directories
profile_dir = Path.home() / ".contextportal" / "playwright_profile"
```

---

## 5. Build & Installation Verification Runbook

To verify that the package builds and packages all submodules cleanly:

```powershell
# 1. Navigate to the backend directory
cd backend

# 2. Perform an editable install
uv pip install -e .

# 3. Verify entrypoint registration
uv run contextportal --help

# 4. Test global isolated installation via uv tool
uv tool install --force .

# 5. Verify global execution
contextportal --help
```

