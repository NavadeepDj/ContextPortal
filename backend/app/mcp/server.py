import asyncio
from mcp.server.mcpserver import MCPServer
import mcp.types as types

# Initialize the MCP Server
mcp = MCPServer("ContextPortal")

@mcp.tool()
async def fetch_context(url: str) -> str:
    """Fetch context from a given URL.
    Can retrieve content from authenticated/protected enterprise portals using the user's secure browser session.
    """
    if not url:
        raise ValueError("url is required")
        
    # Placeholder for Phase B.1
    return "MCP connection successful"

def main():
    """Run the MCP server over STDIO transport."""
    # MCPServer provides a synchronous run method that handles asyncio internally
    mcp.run()

if __name__ == "__main__":
    main()
