---
name: build-python-package
description: >-
  Guides the packaging of the ContextPortal Python backend. Use when modifying 
  pyproject.toml, adding CLI entry points, or fixing package discovery errors 
  (like flat-layout module conflicts).
---

# Build Python Package — ContextPortal

ContextPortal is packaged as a standard Python module managed by `uv` and `setuptools`. It exposes a CLI entrypoint for developers and agents to run the MCP server and login commands.

## 1. CLI Entrypoints

When adding a new command-line tool, define it in `backend/pyproject.toml` under `[project.scripts]`.

```toml
[project.scripts]
contextportal = "app.cli:main"
```

This ensures that running `uv pip install -e .` makes the `contextportal` command globally available in the virtual environment.

## 2. ⚠️ CRITICAL GOTCHA: Package Discovery & Sensitive Data

By default, `setuptools` uses flat-layout auto-discovery. It will look at the `backend/` directory and attempt to package **every** top-level folder as a Python module.

Because ContextPortal creates a `playwright_profile/` directory at runtime (which contains the user's private cookies, local storage, and session state), **auto-discovery will fail** with a "Multiple top-level packages discovered" error, or worse, it might accidentally bundle sensitive user credentials into the distributed package.

### The Fix

You **MUST** explicitly restrict package discovery to the `app/` directory in `pyproject.toml`:

```toml
[tool.setuptools]
packages = ["app"]
```

Never remove this configuration. If you add new source directories (e.g., a `migrations/` folder), you must explicitly add them to this list.

## 3. Testing the Build

After modifying `pyproject.toml` or `app/cli.py`, always rebuild and verify the CLI works:

```powershell
cd backend
uv pip install -e .
uv run contextportal --help
```

If you encounter an error like:
`Call to setuptools.build_meta:__legacy__.build_editable failed... error: Multiple top-level packages discovered`

It means `tool.setuptools.packages` is either missing or misconfigured. Fix it immediately to prevent build failures.

