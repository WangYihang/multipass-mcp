from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from multipass_mcp.multipass import MultipassInfo
from multipass_mcp.multipass import MultipassInstance
from multipass_mcp.server import get_instance_info
from multipass_mcp.server import list_instances
from multipass_mcp.server import start_instance


@pytest.mark.asyncio
async def test_mcp_list_instances():
    with patch('multipass_mcp.server.cli.list_instances', new_callable=AsyncMock) as mock_list:
        mock_instance = MultipassInstance(
            name='test-vm', state='Running', ipv4=['1.2.3.4'], release='22.04',
        )
        mock_list.return_value = [mock_instance]
        result = await list_instances()
        assert result == [mock_instance]
        mock_list.assert_called_once()


@pytest.mark.asyncio
async def test_mcp_start_instance():
    with patch('multipass_mcp.server.cli.start_instance', new_callable=AsyncMock) as mock_start:
        mock_start.return_value = 'Starting test-vm'
        result = await start_instance('test-vm')
        assert result == 'Starting test-vm'
        mock_start.assert_called_with('test-vm')


@pytest.mark.asyncio
async def test_mcp_get_instance_info():
    with patch('multipass_mcp.server.cli.get_info', new_callable=AsyncMock) as mock_info:
        mock_info_obj = MultipassInfo(
            name='test-vm', state='Running', ipv4=['1.2.3.4'], release='22.04',
        )
        mock_info.return_value = mock_info_obj
        result = await get_instance_info('test-vm')
        assert result == mock_info_obj
        mock_info.assert_called_with('test-vm')
