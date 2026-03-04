import asyncio
import json
from dataclasses import dataclass
from dataclasses import field
from typing import Any


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


class MultipassCLI:
    async def _run(self, *args: str) -> str:
        process = await asyncio.create_subprocess_exec(
            'multipass',
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise Exception(f"Multipass error: {stderr.decode().strip()}")
        return stdout.decode().strip()

    async def list_instances(self) -> list[MultipassInstance]:
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

    async def start_instance(self, name: str) -> str:
        return await self._run('start', name)

    async def stop_instance(self, name: str) -> str:
        return await self._run('stop', name)

    async def delete_instance(self, name: str, purge: bool = False) -> str:
        args = ['delete', name]
        if purge:
            args.append('--purge')
        return await self._run(*args)

    async def purge_instances(self) -> str:
        return await self._run('purge')

    async def execute_command(self, name: str, command: str) -> str:
        return await self._run('exec', name, '--', *command.split())

    async def get_info(self, name: str) -> MultipassInfo:
        output = await self._run('info', name, '--format', 'json')
        data = json.loads(output)
        info = data.get('info', {}).get(name, {})
        if not info:
            raise Exception(f"Instance {name} not found")

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
