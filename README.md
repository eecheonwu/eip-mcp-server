# EIP MCP Server

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![MCP Transport](https://img.shields.io/badge/mcp-stdio%20%7C%20http-green.svg)](https://modelcontextprotocol.io/)
[![Framework](https://img.shields.io/badge/framework-FastMCP-purple.svg)](https://github.com/jlowin/fastmcp)

The **EIP MCP Server** is the bridge between your local development environment and the **Engineering Intelligence Platform (EIP)**. It exposes local workspace orchestration capabilities to your AI-powered IDEs via the Model Context Protocol (MCP).

---

## 🚀 About the Engineering Intelligence Platform (EIP)

The **Engineering Intelligence Platform (EIP)** is a modern governance and planning workspace designed for AI-driven software engineering. EIP automatically maintains a Single Source of Truth (SSOT), visualizes architectural knowledge graphs, and governs architectural drift. 

The **EIP MCP Server** empowers AI Coding Agents (such as Antigravity, Claude Desktop, Cursor, or Windsurf) to natively interact with your EIP project.

### How it Connects to EIP
This MCP server operates in a **dual-mode architecture**:
1. **Stdio MCP Interface**: Seamlessly exposes AI tools to your local IDE Agent, allowing it to pull architecture guidelines, parse SSOT requirements, and automatically synchronize your code drift with the remote EIP Knowledge Graph.
2. **Background Webhook Listener**: Upon initialization, the server silently spawns an HTTP listener on port `8123`. This allows the cloud-based **EIP Web App** to trigger deep architectural tasks (like generating an Implementation Plan) which are then executed securely on your local file system.

---

## 🛠️ Available Tools

When connected to your IDE, the AI agent gains access to the following tools:

- `initialize_local_ssot`: Connects to the EIP Web App to scaffold your local `ssot/` directory using the project's Software Requirements Document (SRD).
- `generate_implementation_plan`: Acts as a Staff Engineer. Analyzes local SSOT context and outputs an exhaustive, step-by-step implementation plan.
- `generate_task_plan`: Decompiles the implementation plan into highly specific executable tasks for local agents.
- `generate_test_plan`: Creates comprehensive testing strategies (STQE, RTM) mapped to feature requirements.
- `generate_security_plan`: Generates a rigorous application security plan tailored to the project architecture.
- `synchronize_ssot`: Pushes local documentation and architectural updates back to the EIP Web App's Knowledge Graph to resolve drift.

---

## 📦 Installation & Usage

You can run the server seamlessly using [`uvx`](https://github.com/astral-sh/uv), meaning no manual virtual environments or dependency management is required.

### 1. Direct Execution via `uvx`
If you wish to test the server locally or run it via terminal:

```bash
uvx --from git+https://github.com/eecheonwu/eip-mcp-server.git eip-mcp-server
```

### 2. IDE Configuration (Claude Desktop, Antigravity, etc.)
To give your AI coding assistant full access to the EIP ecosystem, add the following to your IDE's MCP configuration file (e.g., `mcp_config.json` or `claude_desktop_config.json`).

> **⚠️ Important:** The `-q` (quiet) flag is required for `uvx`. Without it, `uvx` build logs will pollute standard output, causing the MCP JSON-RPC initialization handshake to crash.

```json
{
  "mcpServers": {
    "eip-mcp-server": {
      "command": "uvx",
      "args": [
        "-q",
        "--from",
        "git+https://github.com/eecheonwu/eip-mcp-server.git",
        "eip-mcp-server"
      ],
      "env": {
        "GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

#### Supported IDEs:
- **Claude Desktop**: Add to `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS).
- **Antigravity CLI / IDE**: Add to `~/.gemini/config/mcp_config.json`.
- **Cursor**: Configure via Settings > Features > MCP.

---

## 🔧 Architecture Requirements
- **Python**: `3.10` or higher
- **Package Manager**: [uv](https://github.com/astral-sh/uv) by Astral
- **Ports**: Port `8123` must be available for the EIP Webhook Listener.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues).
