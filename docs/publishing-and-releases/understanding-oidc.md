# Understanding OIDC Trusted Publishing for ContextPortal

## 1. Executive Summary & The Core Concept

> **"OIDC lets GitHub Actions prove *who this workflow is* to PyPI using a cryptographic, short-lived identity token, instead of storing a permanent PyPI password or API token in GitHub Secrets."**

For ContextPortal, our primary product thesis is **security, transparency, and credential protection**. Storing a permanent, long-lived API token inside repository secrets conflicts with that philosophy. With **OpenID Connect (OIDC) Trusted Publishing**, zero secrets are stored.

---

## 2. API Tokens vs. OIDC: The "Office Key" Analogy

Think of managing access to a secure server room:

### Without OIDC (Permanent API Token)
You hand your automated deployment system a **physical master key** (`pypi-AgEI...`) and keep it in a lockbox (`GitHub Secrets`).
* **The Vulnerability**: If that secret is leaked, compromised, or accidentally printed to CI logs, an attacker possesses a permanent key to publish malicious versions of your package until you notice and manually revoke it.
* **Maintenance Burden**: Requires key rotation, credential management, and human intervention.

### With OIDC Trusted Publishing
You give GitHub Actions **no keys at all**. Instead, you register a trust rule directly with PyPI:
> *"If a request comes from GitHub repository `NavadeepDj/ContextPortal` running workflow `publish-pypi.yml` from environment `pypi`, grant it temporary access."*

When GitHub Actions runs:
1. It approaches security and presents a cryptographically signed identity pass from GitHub.
2. PyPI verifies the claims (Repository, Workflow, Branch/Tag).
3. PyPI grants a **temporary, single-use access ticket** that expires in minutes.
4. The package is published, and the ticket vanishes.

---

## 3. Comparison Matrix

| Security Dimension | Legacy API Token | OIDC Trusted Publishing |
|---|---|---|
| **Credential Lifetime** | Permanent (until manual revocation) | Temporary (expires in ~15 minutes) |
| **Storage in GitHub** | Stored in Repository Secrets | **Zero secrets stored** |
| **Blast Radius of a Leak** | High (can be used anywhere) | Negligible (bound to CI execution context) |
| **Secret Rotation** | Manual, error-prone | Fully automated & handled by PyPA / GitHub |
| **Authentication Model** | Static credential-based | Cryptographic identity/trust-based |
| **Industry Recommendation** | Phasing out / Legacy | **Modern PyPA & OpenSSF Standard** |

---

## 4. What Claims Does GitHub Actions Present?

When GitHub Actions contacts PyPI, it sends an OIDC JSON Web Token (JWT) signed by GitHub's Certificate Authority containing verifiable claims:

```json
{
  "iss": "https://token.actions.githubusercontent.com",
  "repository": "NavadeepDj/ContextPortal",
  "repository_owner": "NavadeepDj",
  "workflow": "Publish - Production PyPI",
  "job_workflow_ref": "NavadeepDj/ContextPortal/.github/workflows/publish-pypi.yml@refs/tags/v0.1.0",
  "ref": "refs/tags/v0.1.0",
  "environment": "pypi"
}
```

PyPI validates these claims against the **Trusted Publisher configuration** you set up in your PyPI project settings. If they match, the upload is authorized.

---

## 5. Architectural Separation in ContextPortal

We strictly separate our CI/CD workflows so permissions are isolated:

```text
               Code Commit / Pull Request
                          │
                          ▼
            [ .github/workflows/ci.yml ]
            • Matrix testing (Ubuntu + Windows)
            • uv build validation + twine check
            • NO PUBLISHING PERMISSIONS (id-token: none)
                          │
         ┌────────────────┴────────────────┐
         ▼ (Tag: v*rc*)                    ▼ (Tag: v*.*.*)
[ publish-testpypi.yml ]         [ publish-pypi.yml ]
• Requires: id-token: write      • Requires: id-token: write
• Target: test.pypi.org          • Target: pypi.org
• Environment: testpypi          • Environment: pypi
```

By ensuring that `ci.yml` has zero publishing privileges, changes to automated test suites can never accidentally release software to the public registry.

