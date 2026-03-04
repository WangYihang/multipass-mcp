from typing import Any

from fastmcp import FastMCP

from .client import MultipassCLI
from .commands import alias_commands
from .commands import config_commands
from .commands import image_commands
from .commands import instance_commands
from .commands import network_commands
from .commands import snapshot_commands
from .commands import storage_commands
from .models.alias import MultipassAlias
from .models.image import MultipassImage
from .models.instance import MultipassInfo
from .models.instance import MultipassInstance
from .models.network import MultipassNetwork
from .models.snapshot import MultipassSnapshot
from .models.snapshot import MultipassSnapshotInfo
from .models.version import MultipassVersion

# Initialize MCP server
# The name "Multipass" will be shown in MCP clients
mcp = FastMCP(
    'Multipass',
)
cli = MultipassCLI()


@mcp.tool()
async def list_instances() -> list[MultipassInstance]:
    """List all Multipass instances with their current state and IP addresses."""
    return await instance_commands.list_instances(cli)


@mcp.tool()
async def find_images() -> list[MultipassImage]:
    """Find available images for launching new instances."""
    return await image_commands.find_images(cli)


@mcp.tool()
async def launch_instance(
    name: str | None = None,
    image: str | None = None,
    cpus: int | None = None,
    memory: str | None = None,
    disk: str | None = None,
) -> str:
    """
    Launch a new Multipass instance.

    Args:
        name: Optional name for the instance.
        image: Image to use (e.g., '22.04', 'charm-dev', 'docker'). Defaults to latest Ubuntu LTS.
        cpus: Number of CPUs to allocate.
        memory: Amount of memory (e.g., '2G', '512M').
        disk: Disk space (e.g., '10G', '40G').
    """
    return await instance_commands.launch_instance(cli, name, image, cpus, memory, disk)


@mcp.tool()
async def start_instance(name: str) -> str:
    """Start a stopped Multipass instance."""
    return await instance_commands.start_instance(cli, name)


@mcp.tool()
async def stop_instance(name: str) -> str:
    """Stop a running Multipass instance."""
    return await instance_commands.stop_instance(cli, name)


@mcp.tool()
async def restart_instance(name: str | None = None, all_instances: bool = False) -> str:
    """
    Restart Multipass instances.

    Args:
        name: Name of the instance to restart. If omitted and all_instances is False, 'primary' is assumed.
        all_instances: If True, restart all instances.
    """
    return await instance_commands.restart_instance(cli, name, all_instances)


@mcp.tool()
async def suspend_instance(name: str) -> str:
    """Suspend a running Multipass instance, saving its state to disk."""
    return await instance_commands.suspend_instance(cli, name)


@mcp.tool()
async def resume_instance(name: str) -> str:
    """Resume a suspended Multipass instance."""
    return await instance_commands.resume_instance(cli, name)


@mcp.tool()
async def delete_instance(name: str, purge: bool = False) -> str:
    """
    Delete a Multipass instance.

    Args:
        name: Name of the instance to delete.
        purge: If True, immediately purge the instance (cannot be recovered).
    """
    return await instance_commands.delete_instance(cli, name, purge)


@mcp.tool()
async def purge_instances() -> str:
    """Purge all deleted Multipass instances to free up disk space."""
    return await instance_commands.purge_instances(cli)


@mcp.tool()
async def execute_command(name: str, command: str) -> str:
    """
    Execute a shell command inside a Multipass instance.

    Args:
        name: Name of the instance.
        command: The command to run (e.g., 'ls -la', 'uname -a').
    """
    return await instance_commands.execute_command(cli, name, command)


@mcp.tool()
async def get_instance_info(name: str) -> MultipassInfo:
    """Get detailed information about a Multipass instance (CPU, Memory, Disk usage)."""
    return await instance_commands.get_info(cli, name)


@mcp.tool()
async def get_snapshot_info(instance: str, snapshot: str) -> MultipassSnapshotInfo:
    """
    Get detailed information about a Multipass snapshot.

    Args:
        instance: Name of the instance.
        snapshot: Name of the snapshot.
    """
    return await snapshot_commands.get_snapshot_info(cli, instance, snapshot)


@mcp.tool()
async def get_version() -> MultipassVersion:
    """Get Multipass version information for the client and daemon."""
    return await config_commands.get_version(cli)


@mcp.tool()
async def list_networks() -> list[MultipassNetwork]:
    """List host network interfaces available for use with Multipass instances."""
    return await network_commands.list_networks(cli)


@mcp.tool()
async def get_config(key: str | None = None) -> Any:
    """
    Get Multipass configuration settings.

    Args:
        key: The configuration key to retrieve (e.g., 'local.driver'). If omitted, lists all available keys.
    """
    return await config_commands.get_config(cli, key)


@mcp.tool()
async def set_config(key: str, value: str) -> str:
    """
    Set a Multipass configuration setting.

    Args:
        key: The configuration key to set (e.g., 'local.driver').
        value: The value to set for the key.
    """
    return await config_commands.set_config(cli, key, value)


@mcp.tool()
async def clone_instance(source: str, name: str | None = None) -> str:
    """
    Clone an existing instance.

    Args:
        source: The name of the source instance to be cloned.
        name: An optional custom name for the cloned instance.
    """
    return await instance_commands.clone_instance(cli, source, name)


@mcp.tool()
async def mount_directory(
    source: str,
    instance: str,
    target: str | None = None,
    uid_map: list[str] | None = None,
    gid_map: list[str] | None = None,
    mount_type: str | None = None,
) -> str:
    """
    Mount a local directory inside an instance.

    Args:
        source: Path of the local directory to mount.
        instance: Name of the instance.
        target: Optional target mount point inside the instance.
        uid_map: Optional list of UID mappings (host:instance).
        gid_map: Optional list of GID mappings (host:instance).
        mount_type: Type of mount ('classic' or 'native').
    """
    return await storage_commands.mount_directory(cli, source, instance, target, uid_map, gid_map, mount_type)


@mcp.tool()
async def umount_directory(instance: str, path: str | None = None) -> str:
    """
    Unmount a directory from an instance.

    Args:
        instance: Name of the instance.
        path: Optional specific mount point to unmount. If omitted, all mounts are removed.
    """
    return await storage_commands.umount_directory(cli, instance, path)


@mcp.tool()
async def transfer_file(
    source: str,
    destination: str,
    recursive: bool = False,
    parents: bool = False,
) -> str:
    """
    Transfer files/directories between host and instances.

    Args:
        source: Source path (prefix with 'name:' for instance paths).
        destination: Destination path (prefix with 'name:' for instance paths).
        recursive: Recursively copy entire directories.
        parents: Make parent directories as needed.
    """
    return await storage_commands.transfer_file(cli, source, destination, recursive, parents)


@mcp.tool()
async def snapshot_instance(instance: str, name: str | None = None, comment: str | None = None) -> str:
    """
    Take a snapshot of a stopped instance.

    Args:
        instance: The name of the instance.
        name: Optional name for the snapshot.
        comment: Optional comment for the snapshot.
    """
    return await snapshot_commands.snapshot_instance(cli, instance, name, comment)


@mcp.tool()
async def restore_instance(instance: str, snapshot: str, destructive: bool = False) -> str:
    """
    Restore an instance to a previously taken snapshot.

    Args:
        instance: The name of the instance.
        snapshot: The name of the snapshot to restore.
        destructive: If True, discard the current state of the instance.
    """
    return await snapshot_commands.restore_instance(cli, instance, snapshot, destructive)


@mcp.tool()
async def list_snapshots() -> list[MultipassSnapshot]:
    """List all available snapshots."""
    return await snapshot_commands.list_snapshots(cli)


@mcp.tool()
async def recover_instance(name: str | None = None, all_instances: bool = False) -> str:
    """
    Recover deleted instances.

    Args:
        name: Name of the instance to recover.
        all_instances: If True, recover all deleted instances.
    """
    return await instance_commands.recover_instance(cli, name, all_instances)


@mcp.tool()
async def create_alias(
    instance: str,
    command: str,
    alias_name: str | None = None,
    map_working_directory: bool = True,
) -> str:
    """
    Create an alias to be executed on a given instance.

    Args:
        instance: Name of the instance.
        command: Command to execute.
        alias_name: Optional name for the alias. Defaults to command name.
        map_working_directory: If True, automatically map host execution path to mounted path.
    """
    return await alias_commands.create_alias(cli, instance, command, alias_name, map_working_directory)


@mcp.tool()
async def list_aliases() -> list[MultipassAlias]:
    """List available aliases."""
    return await alias_commands.list_aliases(cli)


@mcp.tool()
async def remove_alias(alias_names: list[str] | None = None, all_aliases: bool = False) -> str:
    """
    Remove aliases.

    Args:
        alias_names: Optional list of alias names to remove.
        all_aliases: If True, remove all aliases from current context.
    """
    return await alias_commands.remove_alias(cli, alias_names, all_aliases)


@mcp.tool()
async def switch_alias_context(context_name: str) -> str:
    """
    Switch the current alias context.

    Args:
        context_name: Name of the context to switch to.
    """
    return await alias_commands.switch_alias_context(cli, context_name)


@mcp.tool()
async def authenticate(passphrase: str) -> str:
    """
    Authenticate with the Multipass service.

    Args:
        passphrase: Passphrase provided by a system administrator.
    """
    return await config_commands.authenticate(cli, passphrase)


if __name__ == '__main__':
    mcp.run()
