# EIP MCP Server

An MCP Server to connect with the EIP Web App.

## Installation

You can install this package using `pip` or use it directly with `uvx`:

```bash
# To run via uvx:
uvx --from git+https://github.com/eecheonwu/eip-mcp-server eip-mcp-server
```

## IDE Configuration

To configure this in your Claude Desktop or other MCP-compatible IDE config file, you can add it like this:

```json
{
      "mcpServers": {
        "eip-mcp-server": {
          "command": "uvx",
          "args": [
            "--from",
            "git+https://github.com/eecheonwu/eip-mcp-server.git",
            "eip-mcp-server"
          ],
          "env": {
            "GEMINI_API_KEY": "your-actual-api-key-here"
          }
        }
      }
    }

