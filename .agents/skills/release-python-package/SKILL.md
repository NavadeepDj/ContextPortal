---
name: release-python-package
description: >-
  Rules, conventions, and steps for tagging and releasing ContextPortal to 
  TestPyPI and Production PyPI. Activate when cutting a release, creating git 
  tags, bumping pyproject.toml version, or resolving PyPI publication conflicts.
---

# Release Python Package — ContextPortal

ContextPortal uses an automated GitHub Actions CI/CD pipeline integrated with PyPI / TestPyPI via OpenID Connect (OIDC Trusted Publishing).

---

## 1. ⚠️ CRITICAL RULE: Version Alignment

The Git tag **must** always match the version in `backend/pyproject.toml`, and the commit being tagged **must** contain that exact `pyproject.toml` version.

```
Git Tag:     v0.1.1rc2   ───> Matches ───> pyproject.toml: version = "0.1.1rc2"
Git Tag:     v0.1.0      ───> Matches ───> pyproject.toml: version = "0.1.0"
```

If you tag an earlier commit that still has an older version in `pyproject.toml`, `uv build` will produce the older version filename and PyPI will reject it with:
`400 File already exists`.

---

## 2. ⚠️ CRITICAL RULE: PyPI Immutability

Neither TestPyPI nor Production PyPI allows overwriting existing files.
- Once `0.1.0` or `0.1.1rc1` is published, that exact version string can **never** be used again on that registry.
- Any retry or fix requires bumping the version number (e.g. `rc1` -> `rc2`, or `0.1.0` -> `0.1.1`).

---

## 3. Versioning Standard: PEP 440 + SemVer

Always follow PEP 440 syntax in `backend/pyproject.toml`:
- **Production releases**: `0.1.0`, `0.1.1`, `0.2.0`, `1.0.0`
- **Release Candidates**: `0.1.1rc1`, `0.1.1rc2`
- **Do not use hyphens**: Write `0.1.1rc1`, NOT `0.1.1-rc1`.

---

## 4. Git Tag Routing Matrix

| Tag Pattern | Target Environment | GitHub Action Triggered |
| :--- | :--- | :--- |
| `v*rc*` (e.g. `v0.1.1rc2`) | **TestPyPI** (`testpypi`) | `.github/workflows/publish-testpypi.yml` |
| `v*.*.*` (e.g. `v0.1.0`) | **Production PyPI** (`pypi`) | `.github/workflows/publish-pypi.yml` |

---

## 5. Release Checklist

1. Update version in `backend/pyproject.toml`.
2. Commit and push directly to `origin/main`.
3. Verify that `git log -1` on `origin/main` has the bump commit.
4. Create the tag:
   - **Pre-release**: `git tag vX.Y.ZrcN && git push origin vX.Y.ZrcN` (or GitHub UI as Pre-release).
   - **Production**: `git tag vX.Y.Z && git push origin vX.Y.Z` (or GitHub UI as Latest Release).
5. Watch GitHub Actions workflow run to completion.
6. Verify package on PyPI / TestPyPI.
