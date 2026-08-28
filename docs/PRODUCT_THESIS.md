# ContextPortal — Product Reset & Core Engineering Thesis

## READ THIS BEFORE IMPLEMENTING ANYTHING

ContextPortal is NOT primarily a browser automation product.
ContextPortal is NOT a data warehouse.
ContextPortal is NOT an RAG system.
ContextPortal is NOT an AI summarization platform.
ContextPortal is NOT trying to give an AI agent unrestricted control over the user's browser.

ContextPortal is an **AUTHENTICATED WEB RETRIEVAL LAYER FOR AI AGENTS**.

The central product thesis is:

> Can we make authenticated web retrieval feel as simple to an AI agent as `GET URL`, while giving the agent substantially less access than a general-purpose browser-control system?

Everything we build must be evaluated against this thesis.

---

# 1. The Problem

AI agents can easily retrieve public web pages:

```
Agent
  ↓
GET URL
  ↓
Public website
  ↓
Content
  ↓
Agent
```

But this breaks when the resource is behind:

- login
- OAuth
- SSO
- 2FA
- authenticated sessions
- corporate portals
- learning platforms
- internal documentation
- private dashboards
- subscription/paywalled content
- JavaScript-heavy authenticated applications

The normal web fetcher sees:

```
401 Unauthorized
403 Forbidden
Login Required
Empty SPA shell
CAPTCHA / bot protection
```

The human can see the content because the human has an authorized session.
The agent cannot.

**This is the gap ContextPortal exists to solve.**

---

# 2. The Core Insight

The agent should NOT need to know HOW the page is retrieved.

The agent should not need to know:
- which browser is being used
- how authentication works
- which cookies exist
- whether SSO was used
- whether 2FA was required
- whether the page is rendered by React
- whether Playwright/Puppeteer/CDP is involved
- how redirects work
- how the DOM is extracted

The agent should conceptually think:

```
fetch(url)
```

ContextPortal handles everything necessary behind that interface.

---

# 3. The Desired Experience

```
Agent
  ↓
"Read this URL"
  ↓
ContextPortal
  ↓
Is the resource public?
  │
  ├── YES
  │    ↓
  │    Normal retrieval
  │    ↓
  │    Return content
  │
  └── NO
       ↓
       Is an authorized session available?
       │
       ├── YES
       │    ↓
       │    Retrieve using authorized session
       │    ↓
       │    Extract content
       │    ↓
       │    Return content
       │
       └── NO
            ↓
            Request legitimate user authentication
            ↓
            User authenticates normally
            ↓
            Authorized session established
            ↓
            Retrieve requested resource
            ↓
            Return clean agent-readable context
```

The agent should not need to operate the browser itself for the normal retrieval case.

---

# 4. The Most Important Product Boundary

ContextPortal is NOT:

```
Agent
  ↓
Full browser control
  ↓
Everything the user is logged into
```

Instead:

```
Agent
  ↓
Request specific resource
  ↓
ContextPortal
  ↓
Authorized retrieval
  ↓
ONLY requested resource
  ↓
Clean context
  ↓
Agent
```

The agent should receive access to the RESOURCE, not unrestricted access to the user's identity.

---

# 5. Example

User gives the agent:

```
https://project-dynamo.learn.joinhandshake.com/introduction
```

Normal web retrieval:
```
GET URL → 401 / login → FAILED
```

ContextPortal:
```
URL
  ↓
ContextPortal
  ↓
Detect authentication requirement
  ↓
Use authorized user session
  ↓
Retrieve page
  ↓
Extract meaningful content
  ↓
Normalize to Markdown
  ↓
Return to agent
```

The agent sees something conceptually equivalent to:
```
GET URL → Markdown content
```

The complexity stays behind ContextPortal.

---

# 6. Product Abstraction

The primary abstraction should eventually look conceptually like:

```
context.fetch(url)
```

or:

```
GET /context?url=<target>
```

or through MCP:

```
contextportal.fetch({ "url": "https://..." })
```

The exact interface is NOT decided yet. The important requirement is:

> The agent should need to provide only the resource URL in the common case.

Do not prematurely lock the implementation to HTTP, MCP, CLI, or another transport.
The transport is an implementation detail. The retrieval abstraction is the product.

---

# 7. Public vs Authenticated Retrieval

ContextPortal should eventually implement a retrieval decision tree:

```
URL
  │
  ▼
Validate
  │
  ▼
Attempt normal retrieval
  │
  ├── Success
  │    ↓
  │    Return content
  │
  └── Authentication required
       ↓
       Authorized retrieval path
       ↓
       Return content
```

This means ContextPortal should not unnecessarily use a browser for public pages.

- If normal HTTP retrieval works: use normal HTTP retrieval
- If normal retrieval cannot access the resource because authentication is required: use the authenticated retrieval mechanism

This keeps the system fast and inexpensive.

---

# 8. Browser Is an Implementation Detail

A browser may be required to access authenticated resources. Potential mechanisms include:

- Playwright
- Puppeteer
- Chrome DevTools Protocol
- a browser extension
- an existing user browser session
- a controlled browser profile
- another authenticated browser mechanism

But none of these should become the product abstraction.

The product abstraction is:

```
authenticated resource → agent-readable context
```

NOT:

```
browser automation → agent
```

---

# 9. Local-First MVP

The first MVP should be LOCAL. Do not build cloud infrastructure yet.

Do not build:
- PostgreSQL
- Redis
- Kubernetes
- multi-user infrastructure
- cloud browser fleet
- billing
- organizations
- enterprise administration
- permanent content storage

The goal is to prove the core thesis.

---

# 10. MVP Goal

The first successful demonstration should be:

1. Agent receives a protected URL.
2. ContextPortal attempts normal retrieval.
3. Retrieval requires authentication.
4. ContextPortal uses a legitimate authorized browser/session.
5. User authenticates normally if necessary.
6. ContextPortal retrieves ONLY the requested resource.
7. ContextPortal extracts meaningful content.
8. ContextPortal converts it to clean agent-readable Markdown.
9. Agent receives the content.
10. Agent can continue reasoning using that content.

If all ten steps work, the product thesis is validated.

---

# 11. Do NOT Optimize the MVP for Architecture

The first question is NOT:
> "Is this production-ready?"

The first question is:
> "Does this actually solve the problem?"

We will harden the architecture after proving the core workflow.

This follows:
> Build the right thing before building the thing right.

However, security boundaries that are fundamental to the product should still be respected from the beginning.

---

# 12. MVP Security Boundary

Even in the MVP:

The agent must NOT receive unrestricted browser control.

The MVP should expose only the minimum capability required to:

```
fetch/read a requested resource
```

Avoid exposing arbitrary:
- click
- type
- navigate
- execute JavaScript
- read cookies
- read localStorage
- inspect unrelated tabs
- access arbitrary domains

unless a specific technical requirement proves that such capabilities are necessary.

Browser automation should remain behind the ContextPortal retrieval layer.

---

# 13. Authentication

Authentication must be legitimate.

ContextPortal should NOT:
- bypass authentication
- defeat access controls
- steal credentials
- extract passwords
- bypass MFA
- circumvent authorization
- defeat paywalls through unauthorized means
- evade security controls

The user must authenticate through the normal website flow.
ContextPortal only operates using authorization the user legitimately possesses.

---

# 14. Data Storage Principle

ContextPortal should NOT permanently store private retrieved content by default.

The desired model is:

```
retrieve → extract → deliver → discard temporary content
```

Persistent storage should only be introduced when there is a concrete product requirement.

Do NOT introduce PostgreSQL merely because this is a production-oriented project.
Do NOT introduce a vector database.
Do NOT introduce RAG.
Do NOT introduce embeddings.
Do NOT introduce a permanent document store.

---

# 15. Existing Technology Landscape

There are already projects demonstrating important pieces of this problem:

- **Browser MCP** demonstrates agent access to an already-authenticated real browser session.
- **MCPBrowser** demonstrates authenticated URL fetching and content extraction through a user's browser.
- **Browser automation frameworks** demonstrate authenticated browser control.
- **Other web-retrieval MCPs** demonstrate tiered web-fetch strategies.

Therefore:

> We do NOT need to reinvent authenticated browser access.

The innovation we are exploring is the **RETRIEVAL ABSTRACTION**.

Existing systems tend to expose browser capabilities.
ContextPortal should expose: **"Give me this resource."**

That distinction is central.

---

# 16. Competitive Differentiation

Do NOT position ContextPortal as:
> "Another browser MCP."

Instead:
> "The authenticated fetch layer for AI agents."

The conceptual comparison is:

### Browser automation
```
Agent → Browser tools → Navigate / click / type / scroll / extract
```

### ContextPortal
```
Agent → Fetch resource → ContextPortal → Authentication + retrieval hidden internally → Clean resource context
```

The second abstraction should be simpler for research agents.

---

# 17. Long-Term Vision

The eventual research workflow is:

```
Agent starts research
  ↓
Search web
  ↓
Discover URLs
  ↓
Fetch each source
  │
  ├── Public
  │    ↓
  │    Normal web retrieval
  │
  └── Protected
       ↓
       ContextPortal
       ↓
       Authorized retrieval
       ↓
       Clean context
       │
       └──────────┐
                   ▼
           Unified research
                   ↓
                 Agent
```

The agent should not need to manually distinguish public and private sources.
ContextPortal should make the distinction transparent.

---

# 18. The Ultimate User Experience

The user should eventually be able to say:

> "Research this topic."

The agent discovers:
```
public-source.com/article
internal.company.com/report
handshake.com/course/page
private-research.com/paper
```

The agent can retrieve:
```
public source → normal fetch
internal source → ContextPortal
Handshake source → ContextPortal
private research → ContextPortal
```

The agent receives all authorized information through a consistent retrieval interface.

That is the long-term product.

---

# 19. Development Strategy

Build in this order:

## Phase A — Retrieval Proof
Prove:
```
protected URL → authenticated session → content extraction → Markdown → agent-readable output
```

## Phase B — Agent Interface
Expose the retrieval capability through a minimal agent-facing interface.
MCP is a strong candidate, but do not assume it is the only option before evaluating the actual agent workflow.

## Phase C — Resource Isolation
Ensure:
```
requested URL → ONLY requested resource
```
No unrestricted browser control.

## Phase D — Authentication Session Management
Only after the basic workflow works:
- session lifecycle
- session reuse
- expiration
- revocation
- user isolation

## Phase E — Security Hardening
Add:
- SSRF protection
- origin restrictions
- redirect validation
- authorization boundaries
- content sanitization
- prompt-injection defenses
- auditability

## Phase F — Production Infrastructure
Only after the thesis is validated:
- persistent state where justified
- Redis where justified
- PostgreSQL where justified
- cloud deployment
- scaling
- multi-user support
- observability

---

# 20. Important Engineering Rule

Do not build infrastructure because it "might be useful later."

Every component must answer:

> What concrete MVP problem does this solve?

If the answer is:
> "We may need it in production."

Do not add it yet.

---

# 21. Agent Instructions

Before implementing anything:

1. Read `PROJECT_SPEC.md`.
2. Read `AGENT_RULES.md`.
3. Read `IMPLEMENTATION_PLAN.md`.
4. Read relevant ADRs.
5. Read the OpenWiki documentation.
6. Inspect the existing codebase.
7. Identify what is already implemented.
8. Identify what must change to align the implementation with this product thesis.

Do NOT immediately start coding.

First produce:
- Current architecture
- Current implementation status
- Gap analysis
- Proposed MVP architecture
- Exact next implementation step

Then wait for approval.

---

# 22. Approval Policy

Before requesting approval for any command or consequential action:

Explain:
1. What has already been done.
2. What you plan to do.
3. The exact command/action where practical.
4. Why it helps ContextPortal.
5. Important consequences or risks.
6. Then ask for approval.

Never ask for blind approval.

Do not say:
> "Can I run this?"

without explaining what the command does and why it is necessary.

---

# 23. Verification

Never claim the thesis is proven merely because:
- the browser opened
- login succeeded
- HTML was retrieved
- an endpoint returned 200

The actual success criterion is:

```
AI agent
  ↓
requests protected URL
  ↓
ContextPortal retrieves authorized content
  ↓
agent receives meaningful context
  ↓
agent can use that context in its task
```

The final demonstration must show an agent actually consuming the protected resource.

---

# 24. Current Mission

The immediate mission is NOT:
> "Build a production web application."

The immediate mission is:

> Prove that ContextPortal can turn an authenticated web resource into a normal agent-readable resource with minimal user friction and without granting the agent unrestricted browser access.

Everything else is secondary.

---

# 25. Product Definition

## ContextPortal
### The authenticated fetch layer for AI agents.

Give an agent a URL.

If it is public: fetch it normally.
If it is protected: use the user's legitimate authorized session.

Return: clean, agent-readable, resource-scoped context.

The agent should experience both cases as simply:

```
GET URL
```

**That is the product we are building.**
