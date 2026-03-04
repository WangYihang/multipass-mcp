from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import MultipassCLI


async def mount_directory(
    cli: 'MultipassCLI',
    source: str,
    instance: str,
    target: str | None = None,
    uid_map: list[str] | None = None,
    gid_map: list[str] | None = None,
    mount_type: str | None = None,
) -> str:
    """Mount a directory."""
    args = ['mount']
    if uid_map:
        for mapping in uid_map:
            args.extend(['--uid-map', mapping])
    if gid_map:
        for mapping in gid_map:
            args.extend(['--gid-map', mapping])
    if mount_type:
        args.extend(['--type', mount_type])

    args.append(source)
    mount_target = f"{instance}:{target}" if target else instance
    args.append(mount_target)
    return await cli._run(*args)


async def umount_directory(cli: 'MultipassCLI', instance: str, path: str | None = None) -> str:
    """Unmount a directory."""
    mount = f"{instance}:{path}" if path else instance
    return await cli._run('umount', mount)


async def transfer_file(
    cli: 'MultipassCLI',
    source: str,
    destination: str,
    recursive: bool = False,
    parents: bool = False,
) -> str:
    """Transfer files between host and instance."""
    args = ['transfer']
    if recursive:
        args.append('--recursive')
    if parents:
        args.append('--parents')
    args.extend([source, destination])
    return await cli._run(*args)
