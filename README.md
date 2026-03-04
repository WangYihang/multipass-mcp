# Multipass MCP Server

A Model Context Protocol (MCP) server to manage [Multipass](https://multipass.run/) instances.

## Usage

```bash
claude mcp add --transport stdio multipass -- uvx multipass-mcp
```

## Available Tools

- `list_instances`: List all instances.
- `launch_instance`: Create a new instance.
- `start_instance` / `stop_instance` / `delete_instance`: Manage state.
- `execute_command`: Run commands inside an instance.
- `get_instance_info`: Get detailed specs (CPU, Memory, Disk).
- `purge_instances`: Cleanup deleted instances.
