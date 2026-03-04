import json
import logging
from typing import TYPE_CHECKING

from ..client import MultipassError
from ..models.snapshot import MultipassSnapshot
from ..models.snapshot import MultipassSnapshotInfo

if TYPE_CHECKING:
    from ..client import MultipassCLI

logger = logging.getLogger(__name__)


async def snapshot_instance(
    cli: 'MultipassCLI',
    instance: str,
    name: str | None = None,
    comment: str | None = None,
) -> str:
    """Take a snapshot of a stopped instance."""
    args = ['snapshot', instance]
    if name:
        args.extend(['--name', name])
    if comment:
        args.extend(['--comment', comment])
    return await cli._run(*args)


async def restore_instance(
    cli: 'MultipassCLI',
    instance: str,
    snapshot: str,
    destructive: bool = False,
) -> str:
    """Restore an instance from a snapshot."""
    args = ['restore', f"{instance}.{snapshot}"]
    if destructive:
        args.append('--destructive')
    return await cli._run(*args)


async def list_snapshots(cli: 'MultipassCLI') -> list[MultipassSnapshot]:
    """List all available snapshots."""
    output = await cli._run('list', '--snapshots', '--format', 'json')
    data = json.loads(output)
    snapshots = []
    for instance, snaps in data.get('info', {}).items():
        for snap_name, details in snaps.items():
            snapshots.append(
                MultipassSnapshot(
                    instance=instance,
                    name=snap_name,
                    comment=details.get('comment', ''),
                    parent=details.get('parent', ''),
                ),
            )
    return snapshots


async def get_snapshot_info(cli: 'MultipassCLI', instance: str, snapshot: str) -> MultipassSnapshotInfo:
    """Get detailed info about a snapshot."""
    output = await cli._run('info', f"{instance}.{snapshot}", '--format', 'json')
    data = json.loads(output)
    info = data.get('info', {}).get(instance, {}).get(
        'snapshots', {},
    ).get(snapshot, {})
    if not info:
        logger.warning(
            f"Snapshot '{instance}.{snapshot}' not found in info output",
        )
        raise MultipassError(f"Snapshot {instance}.{snapshot} not found")

    return MultipassSnapshotInfo(
        instance=instance,
        name=snapshot,
        comment=info.get('comment', ''),
        cpu_count=info.get('cpu_count', ''),
        created=info.get('created', ''),
        disk_space=info.get('disk_space', ''),
        memory_size=info.get('memory_size', ''),
        mounts=info.get('mounts', {}),
        parent=info.get('parent', ''),
        size=info.get('size', ''),
    )
