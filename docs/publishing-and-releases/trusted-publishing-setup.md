# GitHub Actions OIDC Trusted Publishing Setup Guide

This guide details how to configure **OIDC Trusted Publishing** between GitHub and PyPI/TestPyPI.

With Trusted Publishing, **no long-lived API tokens or passwords are stored in GitHub Secrets**. Instead, GitHub Actions mints a short-lived OpenID Connect (OIDC) cryptographic token that PyPI verifies against your repository and workflow name.

> 📖 **Deep Dive**: For the full conceptual breakdown and the "Office Key" analogy, read **[`docs/publishing-and-releases/understanding-oidc.md`](understanding-oidc.md)**.

---

## 1. Workflow Architecture Overview

We have separated our automation into three isolated, purpose-built workflows:

```text
.github/workflows/
├── ci.yml                 # Runs on every push / PR to main (Ubuntu + Windows test matrix + uv build validation)
├── publish-testpypi.yml   # Triggers on pre-release tags (v*rc*) -> publishes to TestPyPI
└── publish-pypi.yml       # Triggers on stable release tags (v*.*.*) -> publishes to Production PyPI
```

---

## 2. Setting Up TestPyPI Trusted Publishing

Because `contextportal` is already registered on TestPyPI, you can link it directly in the project settings:

1. Log into **[test.pypi.org](https://test.pypi.org)**.
2. Navigate to your project settings:
   👉 **[test.pypi.org/manage/project/contextportal/settings/publisher/](https://test.pypi.org/manage/project/contextportal/settings/publisher/)**
3. Under **Add a publisher**, configure:
   - **Publisher**: `GitHub`
   - **Owner**: `NavadeepDj`
   - **Repository**: `ContextPortal`
   - **Workflow name**: `publish-testpypi.yml`
   - **Environment name**: `testpypi`
4. Click **Add publisher**.

---

## 3. Setting Up Production PyPI Trusted Publishing

On production PyPI, you configure a "Pending Publisher" before the first upload:

1. Log into **[pypi.org](https://pypi.org)**.
2. Navigate to:
   👉 **[pypi.org/manage/account/publishing/](https://pypi.org/manage/account/publishing/)**
3. Under **Add a pending publisher**, configure:
   - **PyPI Project Name**: `contextportal`
   - **Owner**: `NavadeepDj`
   - **Repository**: `ContextPortal`
   - **Workflow name**: `publish-pypi.yml`
   - **Environment name**: `pypi`
4. Click **Add publisher**.

---

## 4. How to Release

### To Release a Release Candidate (TestPyPI):
Create and push a release candidate tag matching `v*rc*`:
```bash
git tag v0.1.1rc1
git push origin v0.1.1rc1
```
*GitHub Actions automatically runs `publish-testpypi.yml`, builds clean artifacts, exchanges OIDC tokens with TestPyPI, and publishes.*

### To Release a Production Version (PyPI):
Create and push a production release tag:
```bash
git tag v0.1.0
git push origin v0.1.0
```
*GitHub Actions automatically runs `publish-pypi.yml` and publishes directly to PyPI.*

