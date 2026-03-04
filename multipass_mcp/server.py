from fastmcp import FastMCP

from .multipass import MultipassCLI
from .multipass import MultipassInfo
from .multipass import MultipassInstance

# Initialize MCP server
mcp = FastMCP('Multipass')
cli = MultipassCLI()


@mcp.tool()
async def list_instances() -> list[MultipassInstance]:
    """List all Multipass instances."""
    return await cli.list_instances()


@mcp.tool()
async def launch_instance(
    name: str | None = None,
    image: str | None = None,
    cpus: int | None = None,
    memory: str | None = None,
    disk: str | None = None,
) -> str:
    """Launch a new Multipass instance."""
    return await cli.launch_instance(name, image, cpus, memory, disk)


@mcp.tool()
async def start_instance(name: str) -> str:
    """Start a Multipass instance."""
    return await cli.start_instance(name)


@mcp.tool()
async def stop_instance(name: str) -> str:
    """Stop a Multipass instance."""
    return await cli.stop_instance(name)


@mcp.tool()
async def delete_instance(name: str, purge: bool = False) -> str:
    """Delete a Multipass instance."""
    return await cli.delete_instance(name, purge)


@mcp.tool()
async def purge_instances() -> str:
    """Purge all deleted Multipass instances."""
    return await cli.purge_instances()


@mcp.tool()
async def execute_command(name: str, command: str) -> str:
    """Execute a command in a Multipass instance."""
    return await cli.execute_command(name, command)


@mcp.tool()
async def get_instance_info(name: str) -> MultipassInfo:
    """Get detailed information about a Multipass instance."""
    return await cli.get_info(name)

if __name__ == '__main__':
    mcp.run()
