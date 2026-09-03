# PR: feat(packaging): publish contextportal 0.1.0 to TestPyPI & document registry verification

## Summary

This PR officially registers and validates **`contextportal==0.1.0`** on the **TestPyPI** package registry.

It validates our core product thesis: an external user can install `contextportal` purely from a package registry, leave the codebase directory, and immediately retrieve both public and authenticated web content through their AI agent.

---

## What Changed

### 1. Package Configuration & Modern Standards
- **`backend/pyproject.toml`**:
  - Renamed package to canonical public name `contextportal`.
  - Upgraded license format to SPDX `license = "MIT"` (resolved Setuptools deprecation warnings).
  - Configured metadata (keywords, classifiers, project URLs, CLI entrypoint).
- **`backend/README.md`**: Added PyPI-facing quickstart and product overview.
- **`LICENSE`**: Added standard MIT license file.

### 2. Strategic Roadmap & Documentation
- **`PRODUCT_ROADMAP.md`**: Codified the North Star principle (*"One install. One setup. One MCP server. Zero credential handling."*) and outlined Releases 0.1 through 1.0.
- **`docs/testing-python-package/testpypi-test/README.md`**: Complete test report of the live TestPyPI upload, Windows file locking troubleshooting (`os error 32` / `os error 5`), TLS resets on `example.com`, and split-index installation.
- **`docs/building-python-package/from-prototype-to-pypi.md`**: In-depth retrospective chronicling the 8 engineering hurdles overcome from initial local prototype to public registry release.

---

## Test & Verification Matrix

| Test Case | Environment | Command | Status |
|---|---|---|---|
| **Clean Build** | `backend/` | `uv build` | ✅ 0 warnings, 2 artifacts generated |
| **Registry Upload** | TestPyPI | `uv publish --publish-url ...` | ✅ Published (`0.1.0`) |
| **Global Install** | `$env:TEMP` | `uv tool install --index-url ... contextportal` | ✅ Installed 1 executable |
| **Tier 1 (HTTP)** | `$env:TEMP` | `contextportal fetch https://httpbin.org/html` | ✅ Clean markdown, `Auth: False` |
| **Tier 2 (Auth)** | `$env:TEMP` | `contextportal fetch <handshake-url>` | ✅ Handshake task extracted, `Auth: True` |

---

## Next Steps
Following this validation, we will implement **GitHub Actions OIDC Trusted Publishing** for automated releases (`ci.yml`, `publish-testpypi.yml`, and `publish-pypi.yml`).

