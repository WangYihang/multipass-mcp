from fastmcp import FastMCP

from .multipass import MultipassCLI
from .multipass import MultipassImage
from .multipass import MultipassInfo
from .multipass import MultipassInstance

# Initialize MCP server
# The name "Multipass" will be shown in MCP clients
mcp = FastMCP(
    'Multipass',
)
cli = MultipassCLI()


@mcp.tool()
async def list_instances() -> list[MultipassInstance]:
    """List all Multipass instances with their current state and IP addresses."""
    return await cli.list_instances()


@mcp.tool()
async def find_images() -> list[MultipassImage]:
    """Find available images for launching new instances."""
    return await cli.find_images()


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
    return await cli.launch_instance(name, image, cpus, memory, disk)


@mcp.tool()
async def start_instance(name: str) -> str:
    """Start a stopped Multipass instance."""
    return await cli.start_instance(name)


@mcp.tool()
async def stop_instance(name: str) -> str:
    """Stop a running Multipass instance."""
    return await cli.stop_instance(name)


@mcp.tool()
async def suspend_instance(name: str) -> str:
    """Suspend a running Multipass instance, saving its state to disk."""
    return await cli.suspend_instance(name)


@mcp.tool()
async def resume_instance(name: str) -> str:
    """Resume a suspended Multipass instance."""
    return await cli.resume_instance(name)


@mcp.tool()
async def delete_instance(name: str, purge: bool = False) -> str:
    """
    Delete a Multipass instance.

    Args:
        name: Name of the instance to delete.
        purge: If True, immediately purge the instance (cannot be recovered).
    """
    return await cli.delete_instance(name, purge)


@mcp.tool()
async def purge_instances() -> str:
    """Purge all deleted Multipass instances to free up disk space."""
    return await cli.purge_instances()


@mcp.tool()
async def execute_command(name: str, command: str) -> str:
    """
    Execute a shell command inside a Multipass instance.

    Args:
        name: Name of the instance.
        command: The command to run (e.g., 'ls -la', 'uname -a').
    """
    return await cli.execute_command(name, command)


@mcp.tool()
async def get_instance_info(name: str) -> MultipassInfo:
    """Get detailed information about a Multipass instance (CPU, Memory, Disk usage)."""
    return await cli.get_info(name)

if __name__ == '__main__':
    mcp.run()
