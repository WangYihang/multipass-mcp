# Multipass MCP Server

A Model Context Protocol (MCP) server to manage [Multipass](https://multipass.run/) instances.

## Features

- **Robust Command Execution**: Uses `shlex` for safe command parsing.
- **Timeout Support**: Commands have a default timeout of 60s to prevent hanging.
- **Detailed Error Handling**: Custom exceptions and logging for better debugging.
- **Comprehensive Instance Management**: Support for start, stop, suspend, resume, and purge.

## Usage

### Claude Desktop Configuration

Add the following to your Claude configuration:

```json
{
  "mcpServers": {
    "multipass": {
      "command": "uvx",
      "args": ["multipass-mcp"]
    }
  }
}
```

Or via the command line:

```bash
claude mcp add --transport stdio multipass -- uvx multipass-mcp
```

## Available Tools

- `list_instances`: List all instances with their current state and IP addresses.
- `find_images`: Find available images for launching new instances.
- `launch_instance`: Create a new instance with optional CPU, memory, and disk specs.
- `start_instance`: Start a stopped instance.
- `stop_instance`: Stop a running instance.
- `suspend_instance`: Suspend a running instance (saves state to disk).
- `resume_instance`: Resume a suspended instance.
- `delete_instance`: Delete an instance (with optional immediate purge).
- `execute_command`: Run shell commands inside an instance.
- `get_instance_info`: Get detailed specifications and resource usage (CPU, Memory, Disk).
- `purge_instances`: Cleanup all deleted instances to free up disk space.

## Development

### Prerequisites

- [Multipass](https://multipass.run/install) installed and running.
- [uv](https://github.com/astral-sh/uv) for dependency management.

### Running Tests

```bash
uv run pytest
```

### Installation from Source

```bash
uv pip install -e .
```
