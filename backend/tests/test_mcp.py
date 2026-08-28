import pytest
import asyncio
from unittest.mock import patch
from mcp.server.models import InitializationOptions
from mcp.shared.memory import create_client_server_memory_streams
from mcp.client.session import ClientSession
from app.mcp.server import mcp

from unittest.mock import patch, AsyncMock

@pytest.fixture
def mock_get_context():
    with patch("app.mcp.server.get_context", new_callable=AsyncMock) as mock:
        mock.return_value = "# Mocked Content"
        yield mock

@pytest.mark.asyncio
async def test_mcp_fetch_context(mock_get_context):
    # 1. Create in-memory streams for client and server communication
    async with create_client_server_memory_streams() as (client_streams, server_streams):
        # 2. Get the low-level Server instance from the MCPServer wrapper
        server = mcp._lowlevel_server
        
        init_options = InitializationOptions(
            server_name="ContextPortal",
            server_version="0.1.0",
            capabilities=server.get_capabilities(
                notification_options=None,
                experimental_capabilities={}
            )
        )
        
        # 3. Start the server run loop in a background task
        server_task = asyncio.create_task(
            server.run(server_streams[0], server_streams[1], init_options)
        )
        
        try:
            # 4. Create and initialize the client session
            async with ClientSession(client_streams[0], client_streams[1]) as session:
                await session.initialize()
                
                # 5. List tools and verify our tool is registered
                tools_response = await session.list_tools()
                assert len(tools_response.tools) == 1
                assert tools_response.tools[0].name == "fetch_context"
                
                # 6. Call the tool and verify it delegates to get_context
                result = await session.call_tool("fetch_context", {"url": "https://example.com"})
                assert not result.is_error
                assert len(result.content) == 1
                assert result.content[0].type == "text"
                assert result.content[0].text == "# Mocked Content"
                
                mock_get_context.assert_called_once_with("https://example.com")
                
                # 7. Verify security policy enforcement over MCP
                result_local = await session.call_tool("fetch_context", {"url": "http://localhost:8000"})
                # We return the error as a readable string to the LLM
                assert "Error: Access to localhost is forbidden by security policy" in result_local.content[0].text
                
                result_file = await session.call_tool("fetch_context", {"url": "file:///etc/passwd"})
                assert "Error: Invalid scheme" in result_file.content[0].text
        finally:
            # Clean up the background server task
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass
