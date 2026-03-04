import json
from typing import Any
from typing import TYPE_CHECKING

from ..models.version import MultipassVersion

if TYPE_CHECKING:
    from ..client import MultipassCLI


async def get_config(cli: 'MultipassCLI', key: str | None = None) -> dict[str, Any] | str:
    """Get configuration setting(s)."""
    args = ['get']
    if key:
        args.append(key)
    else:
        args.append('--keys')

    output = await cli._run(*args)

    if not key:
        # When getting all keys, it returns a list of keys separated by newlines
        return {'keys': output.splitlines()}

    return output


async def set_config(cli: 'MultipassCLI', key: str, value: str) -> str:
    """Set a configuration setting."""
    return await cli._run('set', f"{key}={value}")


async def get_version(cli: 'MultipassCLI') -> MultipassVersion:
    """Get Multipass version information."""
    output = await cli._run('version', '--format', 'json')
    data = json.loads(output)
    return MultipassVersion(
        multipass=data.get('multipass', ''),
        multipassd=data.get('multipassd', ''),
    )


async def authenticate(cli: 'MultipassCLI', passphrase: str) -> str:
    """Authenticate with the Multipass service."""
    return await cli._run('authenticate', passphrase)
