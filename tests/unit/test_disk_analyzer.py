"""Unit tests for disk space analyzer."""

from typing import Dict
from unittest.mock import Mock, patch

import pytest
from pydantic import BaseModel

from src.domain.models.disk_info import DiskInfo, DiskUsage
from src.domain.services.disk_analyzer import DiskAnalyzer


class TestDiskAnalyzer:
    """Test suite for DiskAnalyzer class."""

    @pytest.fixture
    def disk_analyzer(self) -> DiskAnalyzer:
        """Fixture for DiskAnalyzer instance."""
        return DiskAnalyzer()

    @pytest.fixture
    def mock_disk_usage(self) -> Dict[str, int]:
        """Mock disk usage data."""
        return {
            "total": 500 * 1024 * 1024 * 1024,  # 500 GB
            "used": 250 * 1024 * 1024 * 1024,  # 250 GB
            "free": 250 * 1024 * 1024 * 1024,  # 250 GB
        }

    def test_disk_info_model(self):
        """Test DiskInfo model validation."""
        disk_info = DiskInfo(
            path="/",
            usage=DiskUsage(
                total_bytes=500 * 1024 * 1024 * 1024,
                used_bytes=250 * 1024 * 1024 * 1024,
                free_bytes=250 * 1024 * 1024 * 1024,
            ),
        )
        assert isinstance(disk_info, BaseModel)
        assert disk_info.usage.used_percentage == 50.0

    @patch("psutil.disk_usage")
    def test_get_disk_usage(self, mock_usage, disk_analyzer, mock_disk_usage):
        """Test getting disk usage information."""
        mock_usage.return_value = Mock(
            total=mock_disk_usage["total"],
            used=mock_disk_usage["used"],
            free=mock_disk_usage["free"],
        )

        disk_info = disk_analyzer.get_disk_usage("/")

        assert isinstance(disk_info, DiskInfo)
        assert disk_info.path == "/"
        assert disk_info.usage.total_bytes == mock_disk_usage["total"]
        assert disk_info.usage.used_bytes == mock_disk_usage["used"]
        assert disk_info.usage.free_bytes == mock_disk_usage["free"]
        assert disk_info.usage.used_percentage == 50.0

    @patch("psutil.disk_partitions")
    @patch("psutil.disk_usage")
    def test_get_all_disks(
        self, mock_usage, mock_partitions, disk_analyzer, mock_disk_usage
    ):
        """Test getting information for all mounted disks."""
        mock_partitions.return_value = [
            Mock(device="/dev/disk1", mountpoint="/"),
            Mock(device="/dev/disk2", mountpoint="/home"),
        ]
        mock_usage.return_value = Mock(
            total=mock_disk_usage["total"],
            used=mock_disk_usage["used"],
            free=mock_disk_usage["free"],
        )

        disk_infos = disk_analyzer.get_all_disks()

        assert len(disk_infos) == 2
        assert all(isinstance(info, DiskInfo) for info in disk_infos)
        assert disk_infos[0].path == "/"
        assert disk_infos[1].path == "/home"

    def test_invalid_path(self, disk_analyzer):
        """Test handling of invalid disk path."""
        with pytest.raises(ValueError, match="Invalid disk path"):
            disk_analyzer.get_disk_usage("/nonexistent/path")
