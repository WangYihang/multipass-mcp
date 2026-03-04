import json
from typing import TYPE_CHECKING

from ..models.image import MultipassImage

if TYPE_CHECKING:
    from ..client import MultipassCLI


async def find_images(cli: 'MultipassCLI') -> list[MultipassImage]:
    """Find available images."""
    output = await cli._run('find', '--format', 'json')
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
