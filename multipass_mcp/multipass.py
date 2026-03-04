import asyncio
import json
import logging
import shlex
from dataclasses import dataclass
from dataclasses import field
from typing import Any

# Configure logging
logger = logging.getLogger(__name__)


class MultipassError(Exception):
    """Base exception for Multipass errors."""


class InstanceNotFoundError(MultipassError):
    """Raised when an instance is not found."""


@dataclass
class MultipassInstance:
    name: str
    state: str
    ipv4: list[str]
    release: str


@dataclass
class MultipassInfo:
    name: str
    state: str
    ipv4: list[str]
    release: str
    image_hash: str = ''
    load: list[float] = field(default_factory=list)
    disk_usage: dict[str, str] = field(default_factory=dict)
    memory_usage: dict[str, str] = field(default_factory=dict)
    mounts: dict[str, Any] = field(default_factory=dict)


@dataclass
class MultipassImage:
    name: str
    aliases: list[str]
    os: str
    release: str
    remote: str
    version: str


class MultipassCLI:
    def __init__(self, timeout: float = 60.0):
        self.timeout = timeout

    async def _run(self, *args: str) -> str:
        logger.debug(f"Running Multipass command: multipass {' '.join(args)}")
        try:
            process = await asyncio.wait_for(
                asyncio.create_subprocess_exec(
                    'multipass',
                    *args,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                ),
                timeout=self.timeout,
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                logger.error(f"Multipass error (exit {process.returncode}): {error_msg}")
                raise MultipassError(f"Multipass error: {error_msg}")

            return stdout.decode().strip()
        except asyncio.TimeoutError:
            logger.error(f"Multipass command timed out: {' '.join(args)}")
            raise MultipassError(f"Command timed out after {self.timeout}s")
        except Exception as e:
            if not isinstance(e, MultipassError):
                logger.exception("Unexpected error running Multipass command")
            raise

    async def list_instances(self) -> list[MultipassInstance]:
        """List all instances."""
        output = await self._run('list', '--format', 'json')
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

    async def find_images(self) -> list[MultipassImage]:
        """Find available images."""
        output = await self._run('find', '--format', 'json')
        data = json.loads(output)
        images = []

        # Handle images
        for name, details in data.get('images', {}).items():
            images.append(
                MultipassImage(
                    name=name,
                    aliases=details.get('aliases', []),
                    os=details.get('os', ''),
                    release=details.get('release', ''),
                    remote=details.get('remote', ''),
                    version=details.get('version', ''),
                ),
            )

        # Handle blueprints (often included in find)
        for name, details in data.get('blueprints (deprecated)', {}).items():
            images.append(
                MultipassImage(
                    name=name,
                    aliases=details.get('aliases', []),
                    os=details.get('os', ''),
                    release=details.get('release', ''),
                    remote=details.get('remote', ''),
                    version=details.get('version', ''),
                ),
            )

        return images

    async def start_instance(self, name: str) -> str:
        """Start a stopped instance."""
        return await self._run('start', name)

    async def stop_instance(self, name: str) -> str:
        """Stop a running instance."""
        return await self._run('stop', name)

    async def suspend_instance(self, name: str) -> str:
        """Suspend a running instance."""
        return await self._run('suspend', name)

    async def resume_instance(self, name: str) -> str:
        """Resume a suspended instance."""
        return await self._run('resume', name)

    async def delete_instance(self, name: str, purge: bool = False) -> str:
        """Delete an instance."""
        args = ['delete', name]
        if purge:
            args.append('--purge')
        return await self._run(*args)

    async def purge_instances(self) -> str:
        """Purge all deleted instances."""
        return await self._run('purge')

    async def execute_command(self, name: str, command: str) -> str:
        """Execute a command in an instance."""
        # Use shlex to correctly split commands with quotes/spaces
        cmd_args = shlex.split(command)
        return await self._run('exec', name, '--', *cmd_args)

    async def get_info(self, name: str) -> MultipassInfo:
        """Get detailed info about an instance."""
        output = await self._run('info', name, '--format', 'json')
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
        self,
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
        return await self._run(*args)
