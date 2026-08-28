import asyncio
from mcp.server.mcpserver import MCPServer
import mcp.types as types
from app.core.security import validate_url_policy
from app.core.retriever import get_context

# Initialize the MCP Server
mcp = MCPServer("ContextPortal")

@mcp.tool()
async def fetch_context(url: str) -> str:
    """Fetch context from a given URL.
    Can retrieve content from authenticated/protected enterprise portals using the user's secure browser session.
    """
    if not url:
        raise ValueError("url is required")
        
    try:
        # Enforce security policy before any retrieval
        validate_url_policy(url)
    except ValueError as e:
        # Return a formatted error message so the agent understands why it was blocked.
        # Returning a string prefixed with 'Error:' is a common pattern for LLMs
        # when we can't directly override the is_error flag in the high-level API.
        return f"Error: {str(e)}"
        
    # Delegate entirely to the retrieval orchestrator
    try:
        content = await get_context(url)
        if not content:
            return "Error: Could not retrieve content from the URL. The page might be empty, heavily obfuscated, or the auth session may have expired."
        return content
    except Exception as e:
        return f"Error retrieving context: {str(e)}"

def main():
    """Run the MCP server over STDIO transport."""
    # MCPServer provides a synchronous run method that handles asyncio internally
    mcp.run()

if __name__ == "__main__":
    main()
