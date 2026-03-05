# Multipass MCP Server

A Model Context Protocol (MCP) server to manage [Multipass](https://multipass.run/) instances.

## Usage

### Claude

```bash
claude mcp add --transport stdio multipass -- uvx multipass-mcp
```

Or add the following to your Claude configuration:

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

### Gemini

```bash
gemini mcp add --transport stdio multipass uvx multipass-mcp
```

### Codex

```bash
codex mcp add multipass -- uvx multipass-mcp
```

## Available Tools

The server currently provides comprehensive support for all core Multipass CLI commands, categorized as follows:

### Instance Management
- `list_instances`: List all instances with their current state and IP addresses.
- `launch_instance`: Create a new instance with optional CPU, memory, and disk specs.
- `start_instance`: Start a stopped instance.
- `stop_instance`: Stop a running instance.
- `restart_instance`: Restart running instances.
- `suspend_instance`: Suspend a running instance (saves state to disk).
- `resume_instance`: Resume a suspended instance.
- `delete_instance`: Delete an instance (with optional immediate purge).
- `purge_instances`: Cleanup all deleted instances permanently.
- `recover_instance`: Recover previously deleted instances.
- `clone_instance`: Create an exact copy of an existing instance.
- `execute_command`: Run shell commands inside an instance.
- `get_instance_info`: Get detailed specifications and resource usage (CPU, Memory, Disk).

### Snapshots
- `list_snapshots`: List all available snapshots across instances.
- `get_snapshot_info`: Get detailed information about a specific snapshot.
- `snapshot_instance`: Take a new snapshot of an instance.
- `restore_instance`: Restore an instance from a previously taken snapshot.

### Storage & Files
- `mount_directory`: Mount a local host directory inside an instance.
- `umount_directory`: Unmount a previously mounted directory.
- `transfer_file`: Transfer files or directories between the host and instances.

### Aliases
- `create_alias`: Create an alias to run a specific command on an instance directly from the host.
- `list_aliases`: List all configured aliases in the current context.
- `remove_alias`: Remove one or more existing aliases.
- `switch_alias_context`: Switch to or create a new alias context.

### System, Network & Config
- `find_images`: Find available images for launching new instances.
- `list_networks`: List host network devices available for instance bridging.
- `get_config`: Get global Multipass configuration settings.
- `set_config`: Set global Multipass configuration settings.
- `get_version`: Display version information for the Multipass client and daemon.
- `authenticate`: Authenticate with the Multipass service using a passphrase.

