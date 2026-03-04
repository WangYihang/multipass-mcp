import json
from typing import TYPE_CHECKING

from ..models.network import MultipassNetwork

if TYPE_CHECKING:
    from ..client import MultipassCLI


async def list_networks(cli: 'MultipassCLI') -> list[MultipassNetwork]:
    """List available networks."""
    output = await cli._run('networks', '--format', 'json')
    data = json.loads(output)
    networks = []
    for item in data.get('list', []):
        networks.append(
            MultipassNetwork(
                name=item['name'],
                type=item['type'],
                description=item['description'],
            ),
        )
    return networks
