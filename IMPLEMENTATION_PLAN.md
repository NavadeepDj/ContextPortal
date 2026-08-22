# ContextPortal — Implementation Plan

## Development Strategy

Build the product as a sequence of independently verifiable vertical slices.

Do not attempt to implement the entire system at once.

Each phase must finish with:

- implementation
- tests
- verification
- documentation
- acceptance criteria

---

# PHASE 0 — Repository Bootstrap

## Goal

Create the production-oriented repository foundation.

## Tasks

- Initialize monorepo.
- Create FastAPI backend.
- Create Next.js frontend.
- Configure Python tooling.
- Configure TypeScript tooling.
- Configure PostgreSQL.
- Configure Redis.
- Configure Docker Compose.
- Create `.env.example`.
- Configure linting.
- Configure formatting.
- Configure type checking.
- Configure testing.

## Acceptance Criteria

```text
docker compose up
```

starts the required local services.

Backend health endpoint works.

Frontend loads.

Database connection works.

Redis connection works.

---

# PHASE 1 — Architecture Foundation

## Goal

Establish clean application boundaries.

Implement:

```text
api/
auth/
connectors/
contexts/
security/
storage/
```

Create interfaces for:

```text
AuthenticationProvider
SourceConnector
ContextService
ContextSerializer
```

## Acceptance Criteria

The architecture allows a future connector to be added without modifying the core context delivery system.

---

# PHASE 2 — Database

## Goal

Implement persistent domain models.

Create:

```text
users
sources
auth_sessions
contexts
context_access
audit_logs
```

Implement migrations.

## Acceptance Criteria

- migrations run from clean database
- migrations can be rolled forward
- ownership relationships enforced
- tests verify isolation

---

# PHASE 3 — Security Foundation

## Goal

Implement security before protected URL retrieval.

Build:

### URL validation

- HTTPS requirement where appropriate
- hostname validation
- dangerous scheme rejection

### SSRF protection

Block:

- localhost
- loopback
- private ranges
- link-local
- cloud metadata addresses

Validate redirects.

### Token system

Implement:

```text
generate
hash
validate
expire
revoke
```

## Acceptance Criteria

Security tests demonstrate:

```text
private IP → blocked
metadata endpoint → blocked
malicious redirect → blocked
random valid URL → accepted according to policy
expired token → rejected
revoked token → rejected
```

---

# PHASE 4 — Authentication Session Infrastructure

## Goal

Create isolated authentication-session management.

Implement:

```text
create session
start authentication
track status
expire session
destroy session
```

Design browser session lifecycle.

## Acceptance Criteria

Two users cannot share browser state.

Sessions have explicit expiration.

Sensitive state is not logged.

---

# PHASE 5 — Authenticated Web Connector

## Goal

Create the first source connector.

Implement:

```text
AuthenticatedWebConnector
```

Use Playwright.

Responsibilities:

```text
validate URL
open isolated browser
navigate
detect authentication
allow legitimate authentication
detect successful authentication
navigate to target
retrieve page
close/expire session
```

## Acceptance Criteria

The connector can distinguish:

```text
public page
authenticated page
authentication required
authentication failed
```

---

# PHASE 6 — Handshake MVP

## Goal

Make the real Project Dynamo URL work.

Target:

```text
https://project-dynamo.learn.joinhandshake.com/introduction
```

Do not bypass Handshake authentication.

Do not automate CAPTCHA bypass.

Do not collect Handshake passwords through ContextPortal.

The user authenticates legitimately.

## Acceptance Criteria

Authenticated user can retrieve the authorized Project Dynamo introduction page.

Unauthenticated user cannot retrieve it.

---

# PHASE 7 — Content Extraction

## Goal

Convert retrieved HTML into clean agent-readable content.

Pipeline:

```text
HTML
 ↓
DOM
 ↓
Remove scripts/styles
 ↓
Remove irrelevant UI
 ↓
Identify primary content
 ↓
Preserve semantic structure
 ↓
Markdown
```

Preserve:

- title
- headings
- paragraphs
- lists
- tables
- meaningful links

## Acceptance Criteria

Extracted content is substantially cleaner than raw HTML.

Navigation and scripts are removed.

Semantic headings remain intact.

---

# PHASE 8 — Context Engine

## Goal

Create normalized Context objects.

Implement:

```text
create_context
get_context
expire_context
revoke_context
```

Context should contain:

```text
source metadata
retrieval timestamp
content
content type
expiration
status
```

## Acceptance Criteria

Context can be created from extracted source content.

Context can expire.

Context can be revoked.

---

# PHASE 9 — Secure Context URLs

## Goal

Create the central product primitive.

Example:

```text
https://ctx.example.com/c/<secure-token>
```

Implement:

```text
generate token
hash token
store hash
validate token
check expiration
check revocation
return context
```

## Acceptance Criteria

Valid token retrieves context.

Invalid token fails.

Expired token fails.

Revoked token fails.

Guessing sequential IDs is impossible because identifiers are not used as bearer credentials.

---

# PHASE 10 — Agent Retrieval Endpoint

## Goal

Make the context directly consumable by agents.

Implement:

```text
GET /c/{token}
```

Support:

```text
text/markdown
application/json
```

## Acceptance Criteria

A standard HTTP client can retrieve the context.

The endpoint requires only the context URL/token.

No source credentials are exposed.

---

# PHASE 11 — Frontend MVP

## Goal

Build the minimal user experience.

Screens:

```text
Home
Authentication
Processing
Context Ready
```

Flow:

```text
Paste URL
 ↓
Get Context
 ↓
Authenticate
 ↓
Retrieve
 ↓
Extract
 ↓
Generate context
 ↓
Copy context URL
```

## Acceptance Criteria

A user can complete the entire flow without interacting with the backend manually.

---

# PHASE 12 — End-to-End Testing

## Goal

Automate the complete product flow.

Test:

```text
User
 ↓
Frontend
 ↓
API
 ↓
Authentication
 ↓
Protected source
 ↓
Extraction
 ↓
Context
 ↓
Context URL
 ↓
Agent request
```

Use Playwright for browser-level testing where practical.

---

# PHASE 13 — Security Review

Perform explicit security testing.

## Test

### Authentication

- unauthenticated access
- failed authentication
- expired authentication

### Authorization

- cross-user access
- revoked access
- expired context

### SSRF

- localhost
- private IP
- metadata endpoint
- redirect attacks
- DNS-related edge cases

### Session isolation

- concurrent users
- reused browser context
- session expiration

### Token security

- brute force
- replay after expiration
- replay after revocation

### Content security

- malicious HTML
- script injection
- prompt injection

---

# PHASE 14 — Observability

Implement:

```text
structured logging
request IDs
health endpoint
readiness endpoint
error tracking
basic metrics
```

Track:

```text
authentication failures
retrieval failures
context creation failures
context accesses
latency
```

Never log secrets.

---

# PHASE 15 — Production Containerization

Create production Dockerfiles.

Separate:

```text
frontend
API
browser worker
```

Configure:

```text
PostgreSQL
Redis
secret management
environment configuration
```

---

# PHASE 16 — CI/CD

Create GitHub Actions pipeline.

On every pull request:

```text
lint
 ↓
type check
 ↓
unit tests
 ↓
integration tests
 ↓
security tests
 ↓
build
```

No successful build without passing required checks.

---

# PHASE 17 — Production Deployment

Deploy:

```text
Frontend
Backend
Browser execution
PostgreSQL
Redis
```

Use managed infrastructure where possible.

Configure:

- HTTPS
- domain
- secret manager
- logging
- monitoring
- backups
- database migrations

---

# PHASE 18 — Production Hardening

Review:

- rate limiting
- authentication abuse
- context token abuse
- resource exhaustion
- browser timeouts
- maximum page size
- maximum navigation depth
- concurrent browser limits
- cleanup of expired contexts
- cleanup of expired sessions

---

# PHASE 19 — MCP

Only after the HTTP context primitive is stable.

Create MCP interface for:

```text
get_context
```

Potential future operations:

```text
search_context
refresh_context
list_contexts
```

Do not let MCP bypass existing authorization.

MCP must use the same context/security layer.

---

# PHASE 20 — Additional Connectors

After the Handshake MVP is proven:

Priority candidates:

```text
GitHub
Google Drive
Notion
Slack
Jira
Confluence
```

Every connector must implement the common connector interface.

Do not duplicate context delivery logic.

---

# PHASE 21 — Dynamic Context

Move from static snapshots toward:

```text
Context URL
 ↓
Authorized source
 ↓
Fresh retrieval
 ↓
Normalization
 ↓
Agent
```

Add configurable freshness policies.

---

# PHASE 22 — Enterprise Features

Only after the core product works.

Potential capabilities:

- organization accounts
- team permissions
- SSO
- audit logs
- data retention policies
- admin controls
- connector management
- compliance controls
- enterprise deployment

---

# PHASE 23 — Long-Term Product

The eventual product should expose:

```text
Authenticated Source
        ↓
Authorization
        ↓
Retrieval
        ↓
Normalization
        ↓
Context
        ↓
Secure Delivery
        ↓
Agent
```

Supported interfaces:

```text
HTTP Context URL
MCP
SDK
API
```

---

# Master Definition of Done

The project should not be considered MVP-complete until:

```text
✓ User can submit protected URL
✓ User can authenticate legitimately
✓ Authentication state is isolated
✓ Protected content is retrieved
✓ Content is normalized
✓ Context is stored securely
✓ Context URL is generated
✓ Context URL expires
✓ Context URL can be revoked
✓ Agent can retrieve context
✓ Cross-user access is blocked
✓ SSRF defenses exist
✓ Credentials are never exposed
✓ Browser sessions are isolated
✓ Security tests pass
✓ E2E tests pass
✓ Docker deployment works
✓ CI passes
✓ Documentation exists
```

The final MVP demonstration should be:

```text
Protected Handshake URL
        ↓
Authenticate
        ↓
Retrieve Project Dynamo
        ↓
Generate Context URL
        ↓
Give URL to AI Agent
        ↓
Agent understands Project Dynamo
```

That is the first proof of the ContextPortal thesis.