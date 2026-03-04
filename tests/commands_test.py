import json
from unittest.mock import MagicMock

import pytest

from multipass_mcp.client import InstanceNotFoundError
from multipass_mcp.client import MultipassCLI
from multipass_mcp.commands import alias_commands
from multipass_mcp.commands import config_commands
from multipass_mcp.commands import image_commands
from multipass_mcp.commands import instance_commands
from multipass_mcp.commands import snapshot_commands
from multipass_mcp.commands import storage_commands
from multipass_mcp.models.alias import MultipassAlias
from multipass_mcp.models.image import MultipassImage
from multipass_mcp.models.instance import MultipassInfo
from multipass_mcp.models.instance import MultipassInstance
from multipass_mcp.models.snapshot import MultipassSnapshot
from multipass_mcp.models.snapshot import MultipassSnapshotInfo
from multipass_mcp.models.version import MultipassVersion


@pytest.fixture
def mock_cli():
    cli = MultipassCLI()
    # Use a regular MagicMock to track calls.
    # We will wrap it in a real async function to avoid AsyncMock's internal coroutine warnings.
    cli._run_mock = MagicMock()

    async def _mock_run(*args, **kwargs):
        return cli._run_mock(*args, **kwargs)

    cli._run = _mock_run
    return cli


@pytest.mark.asyncio
async def test_list_instances(mock_cli):
    mock_cli._run_mock.return_value = json.dumps({
        'list': [
            {
                'name': 'test-vm',
                'state': 'Running',
                'ipv4': ['192.168.64.2'],
                'release': 'Ubuntu 22.04 LTS',
            },
        ],
    })

    instances = await instance_commands.list_instances(mock_cli)

    assert len(instances) == 1
    assert isinstance(instances[0], MultipassInstance)
    assert instances[0].name == 'test-vm'
    assert instances[0].state == 'Running'
    mock_cli._run_mock.assert_called_once_with('list', '--format', 'json')


@pytest.mark.asyncio
async def test_get_info(mock_cli):
    mock_cli._run_mock.return_value = json.dumps({
        'info': {
            'test-vm': {
                'state': 'Running',
                'ipv4': ['192.168.64.2'],
                'release': 'Ubuntu 22.04 LTS',
                'image_hash': 'hash123',
                'load': [0.1, 0.2, 0.3],
                'disks': {'sda1': {'total': '10G', 'used': '2G'}},
                'memory': {'total': '2G', 'used': '1G'},
                'mounts': {},
            },
        },
    })

    info = await instance_commands.get_info(mock_cli, 'test-vm')

    assert isinstance(info, MultipassInfo)
    assert info.name == 'test-vm'
    assert info.image_hash == 'hash123'
    mock_cli._run_mock.assert_called_once_with(
        'info', 'test-vm', '--format', 'json',
    )


@pytest.mark.asyncio
async def test_get_info_not_found(mock_cli):
    mock_cli._run_mock.return_value = json.dumps({'info': {}})

    with pytest.raises(InstanceNotFoundError):
        await instance_commands.get_info(mock_cli, 'non-existent')


@pytest.mark.asyncio
async def test_launch_instance(mock_cli):
    mock_cli._run_mock.return_value = 'Launched: test-vm'

    result = await instance_commands.launch_instance(
        mock_cli, name='test-vm', image='22.04', cpus=2, memory='2G', disk='10G',
    )

    assert result == 'Launched: test-vm'
    mock_cli._run_mock.assert_called_once_with(
        'launch', '--name', 'test-vm', '22.04', '--cpus', '2', '--memory', '2G', '--disk', '10G',
    )


@pytest.mark.asyncio
async def test_execute_command(mock_cli):
    mock_cli._run_mock.return_value = 'hello world'

    result = await instance_commands.execute_command(mock_cli, 'test-vm', "echo 'hello world'")

    assert result == 'hello world'
    mock_cli._run_mock.assert_called_once_with(
        'exec', 'test-vm', '--', 'echo', 'hello world',
    )


@pytest.mark.asyncio
async def test_list_snapshots(mock_cli):
    mock_cli._run_mock.return_value = json.dumps({
        'info': {
            'test-vm': {
                'snap1': {'comment': 'test snapshot', 'parent': ''},
            },
        },
    })

    snapshots = await snapshot_commands.list_snapshots(mock_cli)

    assert len(snapshots) == 1
    assert isinstance(snapshots[0], MultipassSnapshot)
    assert snapshots[0].instance == 'test-vm'
    assert snapshots[0].name == 'snap1'
    mock_cli._run_mock.assert_called_once_with(
        'list', '--snapshots', '--format', 'json',
    )


@pytest.mark.asyncio
async def test_get_snapshot_info(mock_cli):
    mock_cli._run_mock.return_value = json.dumps({
        'info': {
            'test-vm': {
                'snapshots': {
                    'snap1': {
                        'comment': 'test',
                        'cpu_count': '2',
                        'created': '2023-01-01',
                        'disk_space': '10G',
                        'memory_size': '2G',
                    },
                },
            },
        },
    })

    info = await snapshot_commands.get_snapshot_info(mock_cli, 'test-vm', 'snap1')

    assert isinstance(info, MultipassSnapshotInfo)
    assert info.name == 'snap1'
    mock_cli._run_mock.assert_called_once_with(
        'info', 'test-vm.snap1', '--format', 'json',
    )


@pytest.mark.asyncio
async def test_snapshot_instance(mock_cli):
    mock_cli._run_mock.return_value = 'Snapshot created'
    await snapshot_commands.snapshot_instance(mock_cli, 'test-vm', name='snap1', comment='test')
    mock_cli._run_mock.assert_called_once_with(
        'snapshot', 'test-vm', '--name', 'snap1', '--comment', 'test',
    )


@pytest.mark.asyncio
async def test_restore_instance(mock_cli):
    mock_cli._run_mock.return_value = 'Restored'
    await snapshot_commands.restore_instance(mock_cli, 'test-vm', 'snap1', destructive=True)
    mock_cli._run_mock.assert_called_once_with(
        'restore', 'test-vm.snap1', '--destructive',
    )


@pytest.mark.asyncio
async def test_create_alias(mock_cli):
    mock_cli._run_mock.return_value = 'Alias created'
    await alias_commands.create_alias(mock_cli, 'test-vm', 'ls', alias_name='my-ls')
    mock_cli._run_mock.assert_called_once_with('alias', 'test-vm:ls', 'my-ls')


@pytest.mark.asyncio
async def test_list_aliases(mock_cli):
    mock_cli._run_mock.return_value = json.dumps({
        'contexts': {
            'default': {
                'my-ls': {'instance': 'test-vm', 'command': 'ls'},
            },
        },
    })

    aliases = await alias_commands.list_aliases(mock_cli)

    assert len(aliases) == 1
    assert isinstance(aliases[0], MultipassAlias)
    assert aliases[0].name == 'my-ls'
    mock_cli._run_mock.assert_called_once_with('aliases', '--format', 'json')


@pytest.mark.asyncio
async def test_remove_alias(mock_cli):
    mock_cli._run_mock.return_value = 'Alias removed'
    await alias_commands.remove_alias(mock_cli, alias_names=['my-ls'])
    mock_cli._run_mock.assert_called_once_with('unalias', 'my-ls')


@pytest.mark.asyncio
async def test_get_config(mock_cli):
    mock_cli._run_mock.return_value = 'virtualbox'
    result = await config_commands.get_config(mock_cli, 'local.driver')
    assert result == 'virtualbox'
    mock_cli._run_mock.assert_called_once_with('get', 'local.driver')


@pytest.mark.asyncio
async def test_get_config_all(mock_cli):
    mock_cli._run_mock.return_value = 'key1\nkey2'
    result = await config_commands.get_config(mock_cli)
    assert result == {'keys': ['key1', 'key2']}
    mock_cli._run_mock.assert_called_once_with('get', '--keys')


@pytest.mark.asyncio
async def test_set_config(mock_cli):
    mock_cli._run_mock.return_value = ''
    await config_commands.set_config(mock_cli, 'local.driver', 'qemu')
    mock_cli._run_mock.assert_called_once_with('set', 'local.driver=qemu')


@pytest.mark.asyncio
async def test_get_version(mock_cli):
    mock_cli._run_mock.return_value = json.dumps({
        'multipass': '1.12.0',
        'multipassd': '1.12.0',
    })
    version = await config_commands.get_version(mock_cli)
    assert isinstance(version, MultipassVersion)
    assert version.multipass == '1.12.0'
    mock_cli._run_mock.assert_called_once_with('version', '--format', 'json')


@pytest.mark.asyncio
async def test_authenticate(mock_cli):
    mock_cli._run_mock.return_value = 'Authenticated'
    await config_commands.authenticate(mock_cli, 'secret')
    mock_cli._run_mock.assert_called_once_with('authenticate', 'secret')


@pytest.mark.asyncio
async def test_mount_directory(mock_cli):
    mock_cli._run_mock.return_value = 'Mounted'
    await storage_commands.mount_directory(
        mock_cli, '/host/path', 'test-vm', target='/guest/path', mount_type='classic',
    )
    mock_cli._run_mock.assert_called_once_with(
        'mount', '--type', 'classic', '/host/path', 'test-vm:/guest/path',
    )


@pytest.mark.asyncio
async def test_transfer_file(mock_cli):
    mock_cli._run_mock.return_value = 'Transferred'
    await storage_commands.transfer_file(
        mock_cli, 'file.txt', 'test-vm:file.txt', recursive=True,
    )
    mock_cli._run_mock.assert_called_once_with(
        'transfer', '--recursive', 'file.txt', 'test-vm:file.txt',
    )


@pytest.mark.asyncio
async def test_find_images(mock_cli):
    mock_cli._run_mock.return_value = json.dumps({
        'images': {
            '22.04': {'release': 'Ubuntu 22.04 LTS', 'version': '20230101'},
        },
        'blueprints (deprecated)': {
            'docker': {'release': 'Docker', 'version': '1.0'},
        },
    })

    images = await image_commands.find_images(mock_cli)

    assert len(images) == 2
    assert isinstance(images[0], MultipassImage)
    assert any(img.name == '22.04' for img in images)
    assert any(img.name == 'docker' for img in images)
    mock_cli._run_mock.assert_called_once_with('find', '--format', 'json')
