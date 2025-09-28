"""
app.py
Main CLI demo application for MCP server integration.
Connects to MCP server, lists resources and capabilities, and
runs a sample word counter tool on user input text.
"""
import os
import asyncio
import sys
from dotenv import load_dotenv
from mcp_client import MCPClient
from utils import format_resources, format_capabilities, handle_error

load_dotenv()  # Load environment variables from .env file if present

# Default environment variable names
SERVER_URL_ENV = "MCP_SERVER_URL"
AUTH_TOKEN_ENV = "MCP_AUTH_TOKEN"

async def main():
    # Get server endpoint and auth from env or arguments
    server_url = os.getenv(SERVER_URL_ENV)
    auth_token = os.getenv(AUTH_TOKEN_ENV)
    headers = {}
    
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    
    # Accept command line arguments for server_url and text input
    import argparse
    parser = argparse.ArgumentParser(description="Demo MCP server integration")
    parser.add_argument("--server-url", type=str, help="MCP server WebSocket endpoint")
    parser.add_argument("--auth-token", type=str, help="Authentication token")
    parser.add_argument("--text", type=str, help="Text to run word counter tool on")
    args = parser.parse_args()
    
    if args.server_url:
        server_url = args.server_url
    
    if args.auth_token:
        auth_token = args.auth_token
        headers["Authorization"] = f"Bearer {auth_token}"
    
    if not server_url:
        print(f"Error: MCP server URL must be specified via --server-url or {SERVER_URL_ENV} env variable.")
        sys.exit(1)
    
    # Initialize MCP client
    client = MCPClient(
        server_url=server_url,
        auth_token=auth_token,
        headers=headers
    )
    
    try:
        await client.connect()
        print("Connected to MCP server.")
        
        resources = await client.list_resources()
        print("\nAvailable Resources:")
        print(format_resources(resources))
        
        capabilities = await client.get_capabilities()
        print("\nServer Capabilities:")
        print(format_capabilities(capabilities))
        
        # Get text input for demo task
        text = args.text
        if not text:
            text = input("\nEnter text to count words (or Ctrl+C to quit): ").strip()
        
        print("\nRunning word counter tool...")
        result = await client.run_word_counter(text)
        print("\nWord Counter Result:")
        print(result)
        
    except Exception as e:
        handle_error(e)
    finally:
        await client.disconnect()
        print("\nDisconnected from MCP server.")

if __name__ == "__main__":
    asyncio.run(main())
