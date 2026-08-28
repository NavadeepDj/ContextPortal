> [!CAUTION]
> **SUPERSEDED**: This document was written before the product reset. The authoritative product definition is now [`docs/PRODUCT_THESIS.md`](docs/PRODUCT_THESIS.md). Sections below that conflict with the thesis (e.g., PostgreSQL as a requirement, token systems for MVP) should be ignored. This file is kept for historical reference only.

# ContextPortal — Product Specification

## 1. Product Identity

### Product name

ContextPortal

### Primary tagline

> Context behind the login? Just send the link.

### Expanded positioning

> Securely turn authenticated web pages, private APIs, and enterprise data into agent-ready context — as easily as sending a link.

---

# 2. Product Vision

AI agents can easily consume publicly accessible URLs.

The problem begins when the useful information is behind:

- authentication
- OAuth
- SSO
- authenticated sessions
- enterprise gateways
- private dashboards
- internal applications
- protected documentation
- private APIs

Today, users have to manually authenticate, find information, copy it, and paste it into their AI agent.

ContextPortal aims to remove that friction.

The fundamental product primitive is:

```text
Protected resource
        ↓
Authorized user
        ↓
ContextPortal
        ↓
Authenticated retrieval
        ↓
Normalized context
        ↓
Secure context URL
        ↓
AI agent
```

The user experience should eventually feel as simple as:

```text
"Here is the link."
```

---

# 3. Core Product Principle

ContextPortal is NOT an authentication bypass.

It operates only on data the user is legitimately authorized to access.

The system must never:

- bypass authentication
- defeat CAPTCHA
- circumvent authorization
- exploit private endpoints
- steal credentials
- impersonate users without authorization
- expose one user's data to another user

The correct flow is:

```text
User
 ↓
Explicit authentication
 ↓
Authorized session
 ↓
Authorized retrieval
 ↓
Agent-readable context
```

---

# 4. Initial MVP

The first target is:

https://project-dynamo.learn.joinhandshake.com/introduction

This URL is intentionally protected.

The MVP must demonstrate that an authenticated user can provide the protected URL, authenticate legitimately, retrieve the content they are authorized to see, transform it into agent-readable context, and expose that context through a secure temporary URL.

---

# 5. MVP Success Criterion

The MVP is successful when the following flow works end-to-end:

```text
User opens ContextPortal
        ↓
Pastes protected Handshake URL
        ↓
System determines authentication is required
        ↓
User authenticates legitimately
        ↓
System obtains authorized browser/session state
        ↓
System navigates to requested page
        ↓
System extracts meaningful content
        ↓
System normalizes content
        ↓
System creates a secure context
        ↓
System generates temporary context URL
        ↓
User gives context URL to an AI agent
        ↓
Agent retrieves context
        ↓
Agent can understand the protected content
```

---

# 6. Product Scope — MVP

## Must have

- Protected URL input
- URL validation
- Authentication flow
- Isolated browser session
- Authenticated page retrieval
- Content extraction
- Markdown normalization
- Context storage
- Secure context token
- Context expiration
- Context revocation
- Agent-readable endpoint
- Basic frontend
- PostgreSQL
- Redis
- Docker
- Automated tests
- Security tests
- Structured logging

## Must NOT be implemented yet

- Multiple OAuth integrations
- Slack integration
- GitHub integration
- Jira integration
- Notion integration
- Vector database
- Embeddings
- RAG
- AI chatbot
- Autonomous multi-agent system
- Billing
- Team collaboration
- Mobile application
- Browser extension
- Complex analytics dashboard

---

# 7. Technical Architecture

Recommended stack:

## Frontend

Next.js + TypeScript

## Backend

Python + FastAPI

## Database

PostgreSQL

## Cache/session coordination

Redis

## Browser automation

Playwright

## Deployment

Containerized services.

---

# 8. High-Level Architecture

```text
                       USER
                        │
                        ▼
                 ┌──────────────┐
                 │   Frontend   │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   FastAPI    │
                 │     API      │
                 └──────┬───────┘
                        │
          ┌─────────────┼──────────────┐
          │             │              │
          ▼             ▼              ▼
     Auth Manager   Context Engine   Security
          │             │              │
          ▼             ▼              ▼
     Playwright     Extraction      Permissions
          │             │              │
          ▼             ▼              ▼
    Protected Web   Normalization   Token System
                        │
                        ▼
                   PostgreSQL
                        │
                        ▼
                     Redis
                        │
                        ▼
                Secure Context URL
                        │
                        ▼
                    AI Agent
```

---

# 9. Architectural Separation

Keep these responsibilities separate:

```text
Authentication
     ↓
Retrieval
     ↓
Normalization
     ↓
Context storage
     ↓
Context delivery
```

A connector must not own the context-sharing system.

The context engine must not depend on a specific provider.

This allows future connectors to be added without rewriting the core system.

---

# 10. Connector Architecture

Define a common interface.

Conceptually:

```python
class SourceConnector:
    async def validate_source(...)
    async def authenticate(...)
    async def get_auth_status(...)
    async def retrieve(...)
    async def revoke(...)
```

Initial implementation:

```text
AuthenticatedWebConnector
```

Future implementations:

```text
GitHubConnector
GoogleDriveConnector
SlackConnector
JiraConnector
NotionConnector
PrivateAPIConnector
```

---

# 11. Authentication Model

Never collect third-party passwords through ContextPortal's own UI.

The system should redirect/open the legitimate provider authentication interface.

Users should authenticate directly with the source.

Authentication state must be isolated per user and per source.

Never share browser sessions between users.

Never place credentials in logs.

---

# 12. Context Model

A Context represents normalized agent-readable information retrieved from a source.

Conceptual structure:

```text
Context
-------
id
user_id
source_id
title
content
content_type
created_at
expires_at
status
```

Possible statuses:

```text
ACTIVE
EXPIRED
REVOKED
```

---

# 13. Context Sharing

The system should generate a cryptographically secure context token.

Example:

```text
https://ctx.example.com/c/abc123...
```

Requirements:

- high entropy
- unpredictable
- expiration
- revocation
- no sequential identifiers
- token hash stored server-side
- access audit logging

The raw token must never be persisted unnecessarily.

---

# 14. Agent Endpoint

The context URL must be directly consumable by agents.

Example:

```text
GET /c/{token}
```

Possible response:

```markdown
# Project Dynamo Introduction

...
```

Support structured JSON as an additional representation.

---

# 15. Context Freshness

MVP may use temporary snapshots.

Initial target:

```text
Context expiration: approximately 1 hour
```

Future versions should support dynamic contexts:

```text
Agent
 ↓
Context URL
 ↓
ContextPortal
 ↓
Authorized source
 ↓
Fresh retrieval
 ↓
Agent
```

---

# 16. Security Requirements

Security is a first-class product requirement.

The system must address:

### SSRF

User-controlled URLs must never be blindly fetched.

Protect against:

- localhost
- loopback addresses
- private IP ranges
- link-local addresses
- cloud metadata endpoints
- malicious redirects
- DNS rebinding

### Session isolation

Each user must receive isolated browser/session state.

### Token security

Tokens must be:

- random
- unguessable
- short-lived
- revocable

### Authorization

Every context request must verify authorization state.

### Logging

Never log:

- passwords
- cookies
- OAuth tokens
- authorization headers
- session secrets
- sensitive document contents

---

# 17. Prompt Injection

Retrieved source content is untrusted data.

Webpage content must never automatically become system-level instructions.

Agent context must remain clearly separated from:

- system instructions
- developer instructions
- agent instructions

---

# 18. Observability

Use structured logs.

Requests should have:

```text
request_id
user_id
source_id
context_id
duration
status
```

Provide:

```text
/health
/ready
```

---

# 19. Product Philosophy

Prefer:

- simple architecture
- deterministic behavior
- explicit interfaces
- strong security
- testability
- observable systems
- small incremental changes

Avoid:

- premature abstraction
- unnecessary AI
- unnecessary microservices
- unnecessary dependencies
- speculative features

---

# 20. Long-Term Vision

ContextPortal should eventually become an authorization-aware context infrastructure layer for AI agents.

The long-term architecture:

```text
                    AI AGENTS
                        │
             ┌──────────┴──────────┐
             │                     │
        Context URL               MCP
             │                     │
             └──────────┬──────────┘
                        │
                 CONTEXT BRIDGE
                        │
       ┌────────────────┼────────────────┐
       │                │                │
     Web             OAuth APIs      Private APIs
       │                │                │
    Handshake         GitHub           Enterprise
    Internal Web     Slack             Systems
    Dashboards       Jira              Databases
       │                │                │
       └────────────────┼────────────────┘
                        │
                  Normalized Context
                        │
                        ▼
                     AI Agent
```

The product is not fundamentally a scraper.

The product is:

> An authorization-aware context layer for AI agents.

---

# 21. Final Product Definition

### One sentence

> ContextPortal lets users turn authenticated resources into agent-readable context as easily as sending a link.

### Tagline

> Context behind the login? Just send the link.