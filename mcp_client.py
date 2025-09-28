"""
mcp_client.py
Provides MCPClient class for interacting with an MCP server.
Supports connection, resource listing, server capability querying, authentication,
and running a demo tool (e.g., word counter) via the MCP protocol.
"""
import os
import asyncio
from mcp import Client
from mcp.types import GetResourcesRequest
from mcp.exceptions import MCPConnectionError, MCPTimeoutError

class MCPClient:
    def __init__(self, server_url, auth_token=None, headers=None, timeout=30, retry_attempts=3):
        """
        Initialize the MCP client.
        Args:
            server_url (str): MCP server WebSocket endpoint.
            auth_token (str, optional): Authentication token for the server.
            headers (dict, optional): Additional headers for authentication.
            timeout (int): Connection timeout in seconds.
            retry_attempts (int): Number of retry attempts for connection.
        """
        self.server_url = server_url
        self.auth_token = auth_token
        self.headers = headers or {}
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.client = None

    async def connect(self):
        """
        Connect to the MCP server.
        """
        try:
            self.client = Client(
                auth_token=self.auth_token,
                headers=self.headers,
                timeout=self.timeout,
                retry_attempts=self.retry_attempts
            )
            await self.client.connect(self.server_url)
        except MCPConnectionError as e:
            raise MCPConnectionError(f"Connection failed: {e}")
        except MCPTimeoutError as e:
            raise MCPTimeoutError(f"Connection timed out: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

    async def disconnect(self):
        """
        Disconnect from the MCP server.
        """
        if self.client:
            await self.client.disconnect()

    async def list_resources(self):
        """
        List available resources from the MCP server.
        """
        if not self.client:
            raise Exception("Not connected to MCP server")
        
        try:
            response = await self.client.list_resources()
            return response
        except Exception as e:
            raise Exception(f"Failed to list resources: {e}")

    async def get_capabilities(self):
        """
        Get server capabilities from the MCP server.
        """
        if not self.client:
            raise Exception("Not connected to MCP server")
        
        try:
            response = await self.client.get_capabilities()
            return response
        except Exception as e:
            raise Exception(f"Failed to get capabilities: {e}")

    async def run_word_counter(self, text):
        """
        Run word counter tool via MCP server.
        Args:
            text (str): Text to count words in.
        Returns:
            Result from the word counter tool.
        """
        if not self.client:
            raise Exception("Not connected to MCP server")
        
        try:
            # Call the word_counter tool on the MCP server
            # This assumes the server exposes a tool named "word_counter"
            result = await self.client.call_tool("word_counter", {"text": text})
            return result
        except Exception as e:
            # Fallback: local word count if server doesn't have the tool
            word_count = len(text.split())
            return {
                "word_count": word_count,
                "character_count": len(text),
                "note": "Calculated locally - server tool not available"
            }
