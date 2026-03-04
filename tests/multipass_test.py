import json
from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from multipass_mcp.multipass import MultipassCLI
from multipass_mcp.multipass import MultipassInfo
from multipass_mcp.multipass import MultipassInstance


@pytest.fixture
def cli():
    return MultipassCLI()


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
async def test_error_handling(cli):
    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b'', b'Error message')
        mock_process.returncode = 1
        mock_exec.return_value = mock_process

        with pytest.raises(Exception) as excinfo:
            await cli.list_instances()
        assert 'Multipass error: Error message' in str(excinfo.value)
