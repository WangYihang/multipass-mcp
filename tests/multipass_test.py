import asyncio
import json
from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from multipass_mcp.multipass import InstanceNotFoundError
from multipass_mcp.multipass import MultipassCLI
from multipass_mcp.multipass import MultipassError
from multipass_mcp.multipass import MultipassImage
from multipass_mcp.multipass import MultipassInfo
from multipass_mcp.multipass import MultipassInstance


@pytest.fixture
def cli():
    return MultipassCLI(timeout=1.0)


@pytest.mark.asyncio
async def test_list_instances(cli):
    mock_output = json.dumps({
        'list': [
            {
                'name': 'test-vm', 'state': 'Running',
                'ipv4': ['192.168.64.2'], 'release': 'Ubuntu 22.04 LTS',
            },
        ],
    })

    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (mock_output.encode(), b'')
        mock_process.returncode = 0
        mock_exec.return_value = mock_process

        result = await cli.list_instances()
        assert len(result) == 1
        assert isinstance(result[0], MultipassInstance)
        assert result[0].name == 'test-vm'
        mock_exec.assert_called_with(
            'multipass', 'list', '--format', 'json',
            stdout=-1, stderr=-1,
        )


@pytest.mark.asyncio
async def test_find_images(cli):
    mock_output = json.dumps({
        'images': {
            '22.04': {
                'aliases': ['jammy'],
                'os': 'Ubuntu',
                'release': '22.04 LTS',
                'remote': '',
                'version': '20230101',
            },
        },
        'blueprints (deprecated)': {
            'docker': {
                'aliases': [],
                'os': '',
                'release': 'Docker',
                'remote': '',
                'version': '1.0',
            },
        },
    })

    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (mock_output.encode(), b'')
        mock_process.returncode = 0
        mock_exec.return_value = mock_process

        result = await cli.find_images()
        assert len(result) == 2
        assert any(img.name == '22.04' for img in result)
        assert any(img.name == 'docker' for img in result)
        assert isinstance(result[0], MultipassImage)


@pytest.mark.asyncio
async def test_get_info(cli):
    mock_output = json.dumps({
        'info': {
            'test-vm': {
                'state': 'Running',
                'ipv4': ['192.168.64.2'],
                'release': 'Ubuntu 22.04 LTS',
                'image_hash': 'hash123',
            },
        },
    })

    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (mock_output.encode(), b'')
        mock_process.returncode = 0
        mock_exec.return_value = mock_process

        result = await cli.get_info('test-vm')
        assert isinstance(result, MultipassInfo)
        assert result.name == 'test-vm'
        assert result.image_hash == 'hash123'


@pytest.mark.asyncio
async def test_get_info_not_found(cli):
    mock_output = json.dumps({'info': {}})

    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (mock_output.encode(), b'')
        mock_process.returncode = 0
        mock_exec.return_value = mock_process

        with pytest.raises(InstanceNotFoundError):
            await cli.get_info('non-existent')


@pytest.mark.asyncio
async def test_start_instance(cli):
    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b'', b'')
        mock_process.returncode = 0
        mock_exec.return_value = mock_process

        await cli.start_instance('test-vm')
        mock_exec.assert_called_with(
            'multipass', 'start', 'test-vm',
            stdout=-1, stderr=-1,
        )


@pytest.mark.asyncio
async def test_execute_command_shlex(cli):
    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b'hello world', b'')
        mock_process.returncode = 0
        mock_exec.return_value = mock_process

        await cli.execute_command('test-vm', 'bash -c "echo hello world"')
        mock_exec.assert_called_with(
            'multipass', 'exec', 'test-vm', '--', 'bash', '-c', 'echo hello world',
            stdout=-1, stderr=-1,
        )


@pytest.mark.asyncio
async def test_error_handling(cli):
    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b'', b'Error message')
        mock_process.returncode = 1
        mock_exec.return_value = mock_process

        with pytest.raises(MultipassError) as excinfo:
            await cli.list_instances()
        assert 'Multipass error: Error message' in str(excinfo.value)


@pytest.mark.asyncio
async def test_timeout(cli):
    with patch('asyncio.create_subprocess_exec') as mock_exec:
        # Mocking asyncio.wait_for to raise TimeoutError
        with patch('asyncio.wait_for', side_effect=asyncio.TimeoutError):
            with pytest.raises(MultipassError) as excinfo:
                await cli.list_instances()
            assert 'Command timed out' in str(excinfo.value)
