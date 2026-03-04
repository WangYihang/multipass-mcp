import json
import logging
import shlex
from typing import TYPE_CHECKING

from ..client import InstanceNotFoundError
from ..models.instance import MultipassInfo
from ..models.instance import MultipassInstance

if TYPE_CHECKING:
    from ..client import MultipassCLI

logger = logging.getLogger(__name__)


async def list_instances(cli: 'MultipassCLI') -> list[MultipassInstance]:
    """List all instances."""
    output = await cli._run('list', '--format', 'json')
    data = json.loads(output)
    instances = []
    for item in data.get('list', []):
        instances.append(
            MultipassInstance(
                name=item['name'],
                state=item['state'],
                ipv4=item['ipv4'],
                release=item['release'],
            ),
        )
    return instances


async def get_info(cli: 'MultipassCLI', name: str) -> MultipassInfo:
    """Get detailed info about an instance."""
    output = await cli._run('info', name, '--format', 'json')
    data = json.loads(output)
    info = data.get('info', {}).get(name, {})
    if not info:
        logger.warning(f"Instance '{name}' not found in info output")
        raise InstanceNotFoundError(f"Instance {name} not found")

    return MultipassInfo(
        name=name,
        state=info.get('state', ''),
        ipv4=info.get('ipv4', []),
        release=info.get('release', ''),
        image_hash=info.get('image_hash', ''),
        load=info.get('load', []),
        disk_usage=info.get('disks', {}),
        memory_usage=info.get('memory', {}),
        mounts=info.get('mounts', {}),
    )


async def launch_instance(
    cli: 'MultipassCLI',
    name: str | None = None,
    image: str | None = None,
    cpus: int | None = None,
    memory: str | None = None,
    disk: str | None = None,
) -> str:
    """Launch a new instance."""
    args = ['launch']
    if name:
        args.extend(['--name', name])
    if image:
        args.append(image)
    if cpus:
        args.extend(['--cpus', str(cpus)])
    if memory:
        args.extend(['--memory', memory])
    if disk:
        args.extend(['--disk', disk])
    return await cli._run(*args)


async def start_instance(cli: 'MultipassCLI', name: str) -> str:
    """Start a stopped instance."""
    return await cli._run('start', name)


async def stop_instance(cli: 'MultipassCLI', name: str) -> str:
    """Stop a running instance."""
    return await cli._run('stop', name)


async def restart_instance(cli: 'MultipassCLI', name: str | None = None, all_instances: bool = False) -> str:
    """Restart an instance."""
    args = ['restart']
    if all_instances:
        args.append('--all')
    elif name:
        args.append(name)
    return await cli._run(*args)


async def suspend_instance(cli: 'MultipassCLI', name: str) -> str:
    """Suspend a running instance."""
    return await cli._run('suspend', name)


async def resume_instance(cli: 'MultipassCLI', name: str) -> str:
    """Resume a suspended instance."""
    return await cli._run('resume', name)


async def delete_instance(cli: 'MultipassCLI', name: str, purge: bool = False) -> str:
    """Delete an instance."""
    args = ['delete', name]
    if purge:
        args.append('--purge')
    return await cli._run(*args)


async def purge_instances(cli: 'MultipassCLI') -> str:
    """Purge all deleted instances."""
    return await cli._run('purge')


async def recover_instance(cli: 'MultipassCLI', name: str | None = None, all_instances: bool = False) -> str:
    """Recover deleted instances."""
    args = ['recover']
    if all_instances:
        args.append('--all')
    elif name:
        args.append(name)
    return await cli._run(*args)


async def execute_command(cli: 'MultipassCLI', name: str, command: str) -> str:
    """Execute a command in an instance."""
    # Use shlex to correctly split commands with quotes/spaces
    cmd_args = shlex.split(command)
    return await cli._run('exec', name, '--', *cmd_args)


async def clone_instance(cli: 'MultipassCLI', source: str, name: str | None = None) -> str:
    """Clone an instance."""
    args = ['clone', source]
    if name:
        args.extend(['--name', name])
    return await cli._run(*args)
