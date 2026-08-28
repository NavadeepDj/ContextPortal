import asyncio
from mcp.server.mcpserver import MCPServer
import mcp.types as types
from app.core.security import validate_url_policy

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
        
    # Placeholder for Phase B.2
    return "MCP connection successful"

def main():
    """Run the MCP server over STDIO transport."""
    # MCPServer provides a synchronous run method that handles asyncio internally
    mcp.run()

if __name__ == "__main__":
    main()
