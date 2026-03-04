from unittest.mock import ANY
from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from multipass_mcp.models.instance import MultipassInfo
from multipass_mcp.models.instance import MultipassInstance
from multipass_mcp.models.snapshot import MultipassSnapshotInfo
from multipass_mcp.server import get_instance_info
from multipass_mcp.server import get_snapshot_info
from multipass_mcp.server import launch_instance
from multipass_mcp.server import list_instances
from multipass_mcp.server import start_instance


@pytest.mark.asyncio
async def test_mcp_list_instances():
    with patch('multipass_mcp.server.instance_commands.list_instances', new_callable=AsyncMock) as mock_list:
        mock_instance = MultipassInstance(
            name='test-vm', state='Running', ipv4=['1.2.3.4'], release='22.04',
        )
        mock_list.return_value = [mock_instance]
        result = await list_instances()
        assert result == [mock_instance]
        mock_list.assert_called_once()


@pytest.mark.asyncio
async def test_mcp_launch_instance():
    with patch('multipass_mcp.server.instance_commands.launch_instance', new_callable=AsyncMock) as mock_launch:
        mock_launch.return_value = 'Launched test-vm'
        result = await launch_instance(name='test-vm', image='22.04')
        assert result == 'Launched test-vm'
        mock_launch.assert_called_once()


@pytest.mark.asyncio
async def test_mcp_start_instance():
    with patch('multipass_mcp.server.instance_commands.start_instance', new_callable=AsyncMock) as mock_start:
        mock_start.return_value = 'Starting test-vm'
        result = await start_instance('test-vm')
        assert result == 'Starting test-vm'
        mock_start.assert_called_with(ANY, 'test-vm')


@pytest.mark.asyncio
async def test_mcp_get_instance_info():
    with patch('multipass_mcp.server.instance_commands.get_info', new_callable=AsyncMock) as mock_info:
        mock_info_obj = MultipassInfo(
            name='test-vm', state='Running', ipv4=['1.2.3.4'], release='22.04',
        )
        mock_info.return_value = mock_info_obj
        result = await get_instance_info('test-vm')
        assert result == mock_info_obj
        mock_info.assert_called_with(ANY, 'test-vm')


@pytest.mark.asyncio
async def test_mcp_get_snapshot_info():
    with patch('multipass_mcp.server.snapshot_commands.get_snapshot_info', new_callable=AsyncMock) as mock_snap_info:
        mock_snap_obj = MultipassSnapshotInfo(
            instance='test-vm', name='snap1', created='2023-01-01',
        )
        mock_snap_info.return_value = mock_snap_obj
        result = await get_snapshot_info('test-vm', 'snap1')
        assert result == mock_snap_obj
        mock_snap_info.assert_called_with(ANY, 'test-vm', 'snap1')
