import asyncio
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from multipass_mcp.client import MultipassCLI
from multipass_mcp.client import MultipassError


@pytest.fixture
def cli():
    return MultipassCLI(timeout=1.0)


@pytest.mark.asyncio
async def test_run_success(cli):
    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b'success output', b'')
        mock_process.returncode = 0
        mock_exec.return_value = mock_process

        result = await cli._run('version')
        assert result == 'success output'
        mock_exec.assert_called_with(
            'multipass', 'version',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )


@pytest.mark.asyncio
async def test_run_error(cli):
    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (b'', b'error message')
        mock_process.returncode = 1
        mock_exec.return_value = mock_process

        with pytest.raises(MultipassError) as excinfo:
            await cli._run('invalid')
        assert 'Multipass error: error message' in str(excinfo.value)


@pytest.mark.asyncio
async def test_run_timeout(cli):
    with patch('asyncio.create_subprocess_exec', new_callable=MagicMock):
        with patch('asyncio.wait_for', side_effect=asyncio.TimeoutError):
            with pytest.raises(MultipassError) as excinfo:
                await cli._run('list')
            assert 'Command timed out' in str(excinfo.value)
