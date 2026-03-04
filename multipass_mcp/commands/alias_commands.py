import json
from typing import TYPE_CHECKING

from ..models.alias import MultipassAlias

if TYPE_CHECKING:
    from ..client import MultipassCLI


async def create_alias(
    cli: 'MultipassCLI',
    instance: str,
    command: str,
    alias_name: str | None = None,
    map_working_directory: bool = True,
) -> str:
    """Create an alias."""
    args = ['alias']
    if not map_working_directory:
        args.append('--no-map-working-directory')
    args.append(f"{instance}:{command}")
    if alias_name:
        args.append(alias_name)
    return await cli._run(*args)


async def list_aliases(cli: 'MultipassCLI') -> list[MultipassAlias]:
    """List available aliases."""
    output = await cli._run('aliases', '--format', 'json')
    data = json.loads(output)
    aliases = []
    for context_name, aliases_data in data.get('contexts', {}).items():
        for alias_name, details in aliases_data.items():
            aliases.append(
                MultipassAlias(
                    name=alias_name,
                    instance=details.get('instance', ''),
                    command=details.get('command', ''),
                    working_directory=details.get('working-directory', ''),
                    context=context_name,
                ),
            )
    return aliases


async def remove_alias(
    cli: 'MultipassCLI',
    alias_names: list[str] | None = None,
    all_aliases: bool = False,
) -> str:
    """Remove aliases."""
    args = ['unalias']
    if all_aliases:
        args.append('--all')
    elif alias_names:
        args.extend(alias_names)
    return await cli._run(*args)


async def switch_alias_context(cli: 'MultipassCLI', context_name: str) -> str:
    """Switch the current alias context."""
    return await cli._run('prefer', context_name)
