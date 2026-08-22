# ADR-001: Ephemeral Context Proxy Architecture

## Status
Accepted

## Context
The original architecture for ContextPortal included PostgreSQL and SQLAlchemy for storing user contexts, authentication sessions, and metadata. However, the core value proposition of ContextPortal is to act as a bridge ("Context behind the login? Just send the link."), allowing AI agents to securely access authenticated resources on behalf of the user. Storing private webpage content permanently on our servers introduces unnecessary security and privacy risks and turns the product into a data warehouse rather than a proxy.

## Decision
We will build ContextPortal as a **stateless/ephemeral context proxy**. 
- **No persistent content storage**: Private webpage/document content will not be stored permanently.
- **No PostgreSQL**: Relational databases are deferred unless a future requirement absolutely justifies them.
- **Redis for ephemeral state**: We will use Redis to handle all temporary state, including authentication sessions, context tokens, expiration, revocation, and rate limiting.
- **Delivery Model**: We will use a Hybrid delivery model. The first agent request triggers a live fetch through an authenticated session, the extracted content is cached briefly in Redis (e.g., 5-minute TTL) for performance, and subsequent requests within the window are served from the cache.

## Consequences
- **Positive**: Significantly stronger privacy and security story ("your data passes through, it doesn't live here").
- **Positive**: Dramatically simpler backend architecture (fewer dependencies, no migrations, less infrastructure).
- **Negative**: We cannot serve historical requests once the cache expires; the agent must request a fresh fetch (which requires the source session to still be valid).
