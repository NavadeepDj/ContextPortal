# Release Versioning, Git Tagging & PyPI Conventions

This guide establishes the versioning, tagging, and publication strategy for ContextPortal across GitHub, TestPyPI, and Production PyPI.

---

## 1. The Three Layers of a Release

A release in ContextPortal involves three tightly coupled layers:

```
┌────────────────────────────────────────────────────────┐
│ 1. Codebase (backend/pyproject.toml)                   │
│    version = "X.Y.Z" or "X.Y.ZrcN" (PEP 440)           │
└──────────────────────────┬─────────────────────────────┘
                           │ built by `uv build`
                           ▼
┌────────────────────────────────────────────────────────┐
│ 2. Git / GitHub Tag (SemVer)                           │
│    vX.Y.Z or vX.Y.ZrcN                                 │
└──────────────────────────┬─────────────────────────────┘
                           │ triggers GitHub Action via OIDC
                           ▼
┌────────────────────────────────────────────────────────┐
│ 3. Target Package Index                                │
│    TestPyPI (pre-release) vs. PyPI (production)        │
└────────────────────────────────────────────────────────┘
```

---

## 2. Versioning Specification: SemVer + PEP 440

ContextPortal follows **Semantic Versioning (SemVer 2.0.0)** mapped directly to Python's **PEP 440** specification.

### Version Components
```
MAJOR . MINOR . PATCH [ PRE-RELEASE ]
  0   .   1   .   0   rc1
```

- **MAJOR (`0.x.x` -> `1.x.x`)**: Breaking architectural changes, incompatible CLI changes, or major public contract revisions.
- **MINOR (`x.1.x` -> `x.2.x`)**: New backward-compatible features (e.g., adding `contextportal setup`, auto-config MCP commands).
- **PATCH (`x.x.1` -> `x.x.2`)**: Backward-compatible bug fixes, security patches, dependency updates.
- **PRE-RELEASE (`rcN`)**: Release Candidate testing phase.

### PyPI Immutability Rule
> **⚠️ CRITICAL**: PyPI and TestPyPI release filenames and versions are **strictly immutable**.
> Once a version (e.g. `0.1.0` or `0.1.1rc2`) is uploaded, it **can NEVER be overwritten or replaced**, even if the release was broken or cancelled. Any new release requires an incremented version number.

### PEP 440 Pre-release Standard vs. SemVer Dashes
- **Python / PyPI Standard (PEP 440)**: Uses direct suffixes:
  - `0.1.1rc1`, `0.1.1rc2` (Release Candidate)
  - `0.1.1a1` (Alpha)
  - `0.1.1b1` (Beta)
- **Do NOT use hyphens for Python package versions**: `0.1.1-rc1` is valid in pure SemVer, but Python packaging tools normalize it to `0.1.1rc1` which can cause discrepancies. Always write `0.1.1rcN` directly in `pyproject.toml`.

---

## 3. Git Tagging Conventions & Workflow Routing

Our CI/CD pipelines use tag pattern matching to automatically direct packages to the proper registry:

| Version Type | Git Tag Pattern | Target Registry | Triggered Workflow |
| :--- | :--- | :--- | :--- |
| **Release Candidate** | `v*rc*` (e.g. `v0.1.1rc2`) | **TestPyPI** | `.github/workflows/publish-testpypi.yml` |
| **Production Release** | `v*.*.*` (e.g. `v0.1.0`) | **Production PyPI** | `.github/workflows/publish-pypi.yml` |

### Why the `v` Prefix?
- Standard Git/GitHub practice prefixes release tags with `v` (e.g. `v0.1.0`).
- The Python package itself is built without `v` (e.g. `0.1.0`).
- The workflows run `uv build` in `backend/` and push whatever version is declared in `backend/pyproject.toml`.

---

## 4. The 5-Step Release Workflow

To ensure zero failed deployments:

### Step 1: Align `pyproject.toml`
Update `backend/pyproject.toml` to the target version:
```toml
[project]
name = "contextportal"
version = "0.1.0"
```

### Step 2: Push to `main`
Commit and push the version bump to GitHub:
```bash
git add backend/pyproject.toml
git commit -m "chore: bump version to 0.1.0"
git push origin main
```

### Step 3: Verify the Commit SHA
Ensure GitHub `main` is at the exact commit containing your version bump before tagging.

### Step 4: Tag & Publish
You can publish via either the GitHub UI or Git CLI:

#### Option A: GitHub Releases UI
1. Go to **Releases** -> **Draft a new release**.
2. Create Tag: `v0.1.0` (Target: `main`).
3. Set Title: `ContextPortal v0.1.0`.
4. Check **"Set as a pre-release"** ONLY if it is an `rc` version.
5. Click **Publish release**.

#### Option B: Git CLI
```bash
# For a test candidate:
git tag v0.1.1rc2
git push origin v0.1.1rc2

# For a production release:
git tag v0.1.0
git push origin v0.1.0
```

### Step 5: Verify in Actions & Registry
1. Monitor the GitHub **Actions** tab.
2. Confirm the OIDC token exchange succeeds (`id-token: write`).
3. Verify the package is live on:
   - TestPyPI: `https://test.pypi.org/project/contextportal/<version>/`
   - PyPI: `https://pypi.org/project/contextportal/<version>/`
