---
name: security-review
description: >-
  Perform a security review checklist on ContextPortal changes. Activate
  before declaring any feature complete, when modifying URL handling,
  authentication, browser sessions, context delivery, API endpoints,
  or any code that touches user data or credentials.
---

# Security Review — ContextPortal

ContextPortal is a security-sensitive product that handles authenticated resources.
Security is a **functional requirement**, not an enhancement.

Run this checklist before declaring any feature or change complete.

---

## 1. SSRF Protection

Any code that fetches a user-provided URL MUST validate it first.

**Check**: Does the change call `validate_url_policy(url)` from `app.core.security` before any fetch?

The policy must reject:
- [ ] Non-HTTP(S) schemes (`file://`, `ftp://`, `data:`, etc.)
- [ ] `localhost` and `localhost.localdomain`
- [ ] Loopback IPs (`127.0.0.1`, `::1`)
- [ ] Private IP ranges (`10.x`, `172.16-31.x`, `192.168.x`)
- [ ] Link-local addresses (`169.254.x`, `fe80::`)
- [ ] Multicast / unspecified addresses
- [ ] Cloud metadata endpoints (`169.254.169.254`)
- [ ] Malicious redirects to any of the above

**Where to look**: `app/core/security.py`, any new code that takes a URL as input.

**Test requirement**: Negative tests must verify that each blocked category raises `ValueError`.

---

## 2. Credential Handling

**NEVER log or persist**:
- [ ] Passwords
- [ ] Session cookies
- [ ] OAuth access/refresh tokens
- [ ] Authorization headers
- [ ] Browser storage containing credentials

**Check**: Search any new `print()`, `logging.*()`, or storage calls for sensitive data.

**Check**: Does the code write to Redis, disk, or database? If so, verify no credentials are stored.

---

## 3. Browser Session Isolation

**Check** (for any Playwright/browser code):
- [ ] Each user gets an isolated browser context
- [ ] No shared persistent profiles across users
- [ ] Browser context is always closed in a `finally` block
- [ ] No cross-user session reuse
- [ ] `browser_context.close()` is called even on exceptions

**Reference**: `app/core/retriever.py` — `_fetch_authenticated_sync` uses `launch_persistent_context` with a local `playwright_profile` directory.

---

## 4. Transparent Automation (ADR-003)

ContextPortal uses the user's real Chrome (`channel="chrome"`) and does NOT hide automation.

**NEVER**:
- [ ] Spoof User-Agent to hide automation
- [ ] Disable `AutomationControlled` blink feature
- [ ] Hide `navigator.webdriver`
- [ ] Inject stealth scripts
- [ ] Bypass CAPTCHA
- [ ] Defeat bot detection

**If a provider blocks the automated window**, that is the expected behavior. Document it, don't circumvent it.

---

## 5. Context Token Security

If the change involves context tokens or context URLs:
- [ ] Tokens use high-entropy random values (e.g., `secrets.token_urlsafe`)
- [ ] Tokens are unpredictable (no sequential IDs like `/context/1`, `/context/2`)
- [ ] Tokens expire automatically
- [ ] Tokens support revocation
- [ ] Token hashes are stored, not raw bearer tokens
- [ ] Every context request validates: `exists AND valid AND not expired AND not revoked`

---

## 6. Authorization

- [ ] Every context access verifies the requester is authorized
- [ ] Never trust client-provided user IDs
- [ ] Never trust client-provided ownership claims
- [ ] Cross-tenant access fails closed (User A cannot see User B's context)

**Test requirement**: Explicitly test `User A → User B context = denied`.

---

## 7. Retrieved Content Safety

All fetched webpage content is **untrusted data**.

- [ ] Content is never interpreted as system/developer/agent instructions
- [ ] Content is never executed (no `eval`, no template injection)
- [ ] Content is sanitized during markdown conversion (scripts/styles stripped)

**Reference**: `extract_markdown()` in `retriever.py` strips `script` and `style` tags.

---

## 8. API Endpoint Safety

For any new or modified API endpoint:
- [ ] Uses typed request models (Pydantic)
- [ ] Uses typed response models
- [ ] Has explicit error responses
- [ ] Validates input at the boundary
- [ ] Does NOT expose internal database models directly
- [ ] Error responses don't leak stack traces, tokens, or credentials

---

## 9. Error Handling

- [ ] Errors fail safely (deny access by default)
- [ ] Error messages don't leak secrets, tokens, or internal paths
- [ ] Production responses don't include stack traces
- [ ] Sensitive content is never included in error responses

---

## 10. Negative Test Verification

Every security-sensitive component MUST have negative tests:

```python
# Example: verify blocked URL raises error
def test_rejects_localhost():
    with pytest.raises(ValueError, match="forbidden by security policy"):
        validate_url_policy("http://localhost:8000")

# Example: verify cross-tenant access denied
def test_user_a_cannot_access_user_b_context():
    # ... setup user A and user B contexts
    # ... assert user A gets 403 for user B's context
```

---

## Quick Checklist (Copy-Paste)

```markdown
## Security Review for [Feature Name]

- [ ] SSRF: All user URLs pass through `validate_url_policy()`
- [ ] Credentials: No secrets logged or persisted
- [ ] Sessions: Browser contexts are isolated and cleaned up
- [ ] Automation: No stealth flags or bot-detection evasion
- [ ] Tokens: High-entropy, expiring, revocable, hash-stored
- [ ] Authorization: Every access is verified, cross-tenant denied
- [ ] Content: Fetched content treated as untrusted data
- [ ] API: Typed models, input validation, safe error responses
- [ ] Errors: Fail safe, no secret leakage
- [ ] Tests: Negative tests for all security paths
```
