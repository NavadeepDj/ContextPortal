# [Release 0.1] TestPyPI Registry Distribution & Verification

## 1. Objective & Context
Transition ContextPortal from a locally-built source package into an officially published, globally resolvable distribution on **TestPyPI** ([test.pypi.org/project/contextportal](https://test.pypi.org/project/contextportal)).

The goal was to execute the complete **"Stranger Test (Registry Edition)"**:
- Reserve and verify the canonical `contextportal` package namespace.
- Ensure package builds comply with modern packaging standards (PEP 517/518/621, SPDX license expressions).
- Validate that an external user can run `uv tool install` pointing to the public package index and execute dual-tier retrieval from an isolated directory (`$env:TEMP`) with zero source dependencies.

---

## 2. Key Accomplishments

### A. Packaging & Metadata Audit
- **Canonical Naming**: Updated package name from internal `contextportal-backend` to `contextportal`.
- **Modern Standards**: Migrated legacy license tables to modern SPDX expression (`license = "MIT"`) and cleaned up deprecated classifiers.
- **PyPI Presentation**: Added [`backend/README.md`](../../backend/README.md) and [`LICENSE`](../../LICENSE) for clean rendering on index pages.

### B. Registry Publication
- Successfully compiled source distribution (`.tar.gz`) and universal wheel (`.whl`) via `uv build`.
- Published `contextportal==0.1.0` to TestPyPI via `uv publish`.

### C. Live Registry Stranger Test (`$env:TEMP`)
- Installed globally via:
  ```powershell
  uv tool install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ contextportal
  ```
- **Tier 1 (Fast HTTP)**: Successfully retrieved public content (`https://httpbin.org/html`) with transparent `ContextPortal/0.1.0` User-Agent.
- **Tier 2 (Session Fallback)**: Successfully detected auth wall on Handshake portal and extracted sanitized Markdown via persistent local Chrome session.

---

## 3. Roadblocks Documented & Resolved
1. **Windows Process Locking (`os error 32` & `os error 5`)**: Resolved by terminating active background STDIO MCP server processes before updating entrypoints.
2. **Corporate TLS Handshake Drops**: Diagnosed and documented corporate network/proxy TLS resets on RFC-reserved documentation domains (`example.com`).
3. **Split-Index Resolution**: Documented `--extra-index-url` usage for installing from TestPyPI alongside standard PyPI dependencies.

---

## 4. Verification Checklist
- [x] Clean build with 0 deprecation warnings
- [x] Package live on TestPyPI registry
- [x] Global installation verified outside repository
- [x] Fast HTTP retrieval verified
- [x] Authenticated session retrieval verified
- [x] Zero credential exposure confirmed

