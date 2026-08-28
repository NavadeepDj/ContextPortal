# Phase B.2: Security & URL Policy

## The Threat: What is SSRF?
Before MCP, a **human** typed the URL into ContextPortal. Now, an **AI Agent** controls the URL. This fundamentally changes the security profile of the application. 

If we blindly pass any URL the agent provides into our retrieval engine, the agent could trick the application into making unauthorized requests to internal systems. This vulnerability is called **Server-Side Request Forgery (SSRF)**. 

For example, an attacker could instruct the LLM to:
- Read local files: `file:///etc/passwd` or `file:///C:/Windows/System32/drivers/etc/hosts`
- Scan internal network databases: `http://192.168.1.100:5432`
- Access local development servers: `http://localhost:8000/api/admin`

ContextPortal's core promise is to retrieve *authenticated web context*, not to act as an unrestricted proxy into the user's private computer or enterprise network.

## The Objective
We must establish a strict security boundary at the very edge of the application (inside the MCP tool) that rejects dangerous URLs *before* the retrieval engine ever sees them.

## Implementation Details

### The Policy Rules (`backend/app/core/security.py`)
We implemented a `validate_url_policy(url: str)` function that acts as a strict whitelist/blacklist filter:

1. **Allowed Schemes**: 
   - We only permit `http://` and `https://`. 
   - We explicitly reject `file://`, `javascript://`, `data://`, and `ftp://`.
2. **Localhost Blocking**: 
   - We explicitly block the exact strings `localhost` and `localhost.localdomain`.
3. **Private & Internal IP Blocking**: 
   - Hackers often bypass string filters by passing direct IP addresses (e.g., `http://127.0.0.1` instead of `http://localhost`).
   - We use Python's built-in `ipaddress` library to parse the hostname. 
   - We aggressively block any IP that is:
     - **Loopback**: `127.0.0.0/8`, `::1`
     - **Private (RFC 1918)**: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`
     - **Link-local**, **Multicast**, or **Unspecified**.

*(Note: In Phase B.2, we are establishing the primary boundary. We are not yet implementing complex enterprise DNS rebinding protections, which are out of scope for a local MVP).*

### Legible AI Error Handling
When a human sees an error, a red screen is fine. When an LLM sees an error, it needs to understand *why* so it can correct its behavior.

If the agent requests `http://localhost:8000`, the `validate_url_policy` raises a `ValueError`. 
Instead of letting the MCP protocol crash and return a generic "UnexpectedToolError" (which gives the LLM zero context), our `fetch_context` tool explicitly catches the error and returns it as a formatted string:
```text
"Error: Access to localhost is forbidden by security policy"
```
By returning the exact reason, the LLM knows its request was blocked for security reasons, preventing it from retrying the same URL endlessly or hallucinating a response.

## How We Tested It
- **Unit Tests (`test_security.py`)**: We pass dozens of edge-case URLs (public, file, loopback, private IPs) directly into `validate_url_policy` to mathematically prove the IP ranges are blocked.
- **Integration Tests (`test_mcp.py`)**: We use the in-memory MCP client to simulate an AI agent requesting blocked URLs. We verify that the formatted `"Error: ..."` string is successfully transmitted back over the protocol layer.

