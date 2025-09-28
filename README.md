# mcp-app-integration-demo

Demo repo for integrating an MCP server to use an external application/tool.

## What is MCP (Model Context Protocol)?

MCP is an open protocol that enables AI applications and models to securely access external data sources and tools. It provides a standardized way for AI systems to interact with various services, databases, and applications.

## Initial Steps to Connect to an MCP Server

### Prerequisites

- Python 3.8 or higher
- `mcp` Python package
- Access to an MCP server endpoint

### Installation

```bash
pip install mcp
```

### Basic Connection Setup

1. **Import Required Modules**
   ```python
   from mcp import Client
   from mcp.types import GetResourcesRequest
   import asyncio
   ```

2. **Initialize MCP Client**
   ```python
   async def connect_to_mcp_server():
       # Replace with your MCP server URL
       server_url = "ws://localhost:8080/mcp"
       
       client = Client()
       await client.connect(server_url)
       
       return client
   ```

3. **Basic Server Communication**
   ```python
   async def get_server_info(client):
       # Get available resources from the server
       response = await client.list_resources()
       print("Available resources:", response)
       
       # Get server capabilities
       capabilities = await client.get_capabilities()
       print("Server capabilities:", capabilities)
   ```

4. **Complete Example**
   ```python
   import asyncio
   from mcp import Client
   
   async def main():
       try:
           # Connect to MCP server
           client = await connect_to_mcp_server()
           
           # Get server information
           await get_server_info(client)
           
           # Your application logic here
           
           # Close connection
           await client.disconnect()
       except Exception as e:
           print(f"Error connecting to MCP server: {e}")
   
   if __name__ == "__main__":
       asyncio.run(main())
   ```

### Configuration Options

#### Authentication
```python
# For servers requiring authentication
client = Client(
    auth_token="your-auth-token",
    headers={"Authorization": "Bearer your-token"}
)
```

#### Timeout Settings
```python
client = Client(
    timeout=30,  # Connection timeout in seconds
    retry_attempts=3
)
```

### Common Use Cases

1. **Database Access**: Connect to databases through MCP for secure data retrieval
2. **API Integration**: Access external APIs through MCP servers
3. **File Operations**: Perform file system operations via MCP
4. **Tool Execution**: Execute external tools and applications

### Error Handling

```python
from mcp.exceptions import MCPConnectionError, MCPTimeoutError

try:
    client = await connect_to_mcp_server()
except MCPConnectionError as e:
    print(f"Connection failed: {e}")
except MCPTimeoutError as e:
    print(f"Connection timed out: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Next Steps

1. Review your MCP server documentation for specific endpoints
2. Implement proper error handling and logging
3. Set up configuration management for different environments
4. Add authentication and security measures as needed
5. Test the integration thoroughly

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the [MIT License](LICENSE).
