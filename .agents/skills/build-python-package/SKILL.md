---
name: build-python-package
description: >-
  Guides the packaging and CLI testing of the ContextPortal Python backend. 
  Use when modifying pyproject.toml, adding CLI entry points, fixing package 
  discovery errors (like flat-layout conflicts or omitted subpackages), or 
  validating global installations.
---

# Build & Test Python Package — ContextPortal

ContextPortal is packaged as a standard Python module managed by `uv` and `setuptools`. It exposes a CLI entrypoint (`contextportal`) for developers and agents to run the MCP server, pre-warm login sessions, and test fetches.

---

## 1. CLI Entrypoints

When adding a new command-line tool, define it in `backend/pyproject.toml` under `[project.scripts]`.

```toml
[project.scripts]
contextportal = "app.cli:main"
```

---

## 2. ⚠️ CRITICAL GOTCHA: Recursive Package Discovery

By default, `setuptools` uses flat-layout auto-discovery. It will look at the `backend/` directory and attempt to package **every** top-level folder as a Python module.

Because ContextPortal creates runtime folders (like `playwright_profile/` containing sensitive cookies and session state), **auto-discovery will fail** with a "Multiple top-level packages discovered" error, or risk bundling user credentials into the distribution package.

### The Fix
You **MUST** explicitly specify recursive package discovery for `app` and all nested subpackages (`app.core`, `app.mcp`, etc.):

```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["app", "app.*"]
```

> ⚠️ **Warning**: Do not use `packages = ["app"]`. That static syntax only packages the root folder and omits `app/core/` and `app/mcp/`, causing runtime `ModuleNotFoundError` crashes.

---

## 3. ⚠️ CRITICAL GOTCHA: Avoid Relative Paths for CLI State

When developing a CLI tool, users will run the command from arbitrary directories across their system. 

**Never** use relative paths (`./`) for saving configuration, caching, or user sessions. If you do, state will be fragmented across every directory the user runs the tool from.

```python
# ❌ WRONG (State is fragmented based on CWD)
profile_dir = Path("./playwright_profile")

# ✅ CORRECT (State is globally consistent across all working directories)
profile_dir = Path.home() / ".contextportal" / "playwright_profile"
```

---

## 4. Verification Workflow

After modifying `pyproject.toml` or `app/cli.py`, always rebuild and verify the CLI works both locally and globally:

```powershell
# 1. Local editable test
cd backend
uv pip install -e .
uv run contextportal --help

# 2. Global isolated stranger test (from outside the repo)
uv tool install --force .
contextportal --help
contextportal fetch https://example.com
```
