"""Test module for disk analyzer."""

import os
import shutil
from unittest.mock import Mock, patch

import pytest

from src.domain.models.disk_info import DiskInfo
from src.domain.services.disk_analyzer import DiskAnalyzer


def test_disk_info_model():
    """Test DiskInfo model creation."""
    disk_info = DiskInfo(
        path="/test",
        total_space=1000,
        used_space=500,
        free_space=500,
    )
    assert disk_info.path == "/test"
    assert disk_info.total_space == 1000
    assert disk_info.used_space == 500
    assert disk_info.free_space == 500
    assert disk_info.used_percentage == 50.0


def test_get_disk_usage():
    """Test getting disk usage for a path."""
    analyzer = DiskAnalyzer()
    with (
        patch("os.path.exists", return_value=True),
        patch("os.access", return_value=True),
        patch("shutil.disk_usage") as mock_disk_usage,
    ):
        mock_disk_usage.return_value = shutil._ntuple_diskusage(1000, 500, 500)
        info = analyzer.get_disk_usage("/test")
        assert info.path == "/test"
        assert info.total_space == 1000
        assert info.used_space == 500
        assert info.free_space == 500


def test_get_all_disks():
    """Test getting all disk information."""
    analyzer = DiskAnalyzer()
    with (
        patch("os.path.exists", return_value=True),
        patch("os.access", return_value=True),
        patch("shutil.disk_usage") as mock_disk_usage,
    ):
        mock_disk_usage.return_value = shutil._ntuple_diskusage(1000, 500, 500)
        disks = analyzer.get_all_disks()
        assert len(disks) > 0
        for disk in disks:
            assert isinstance(disk, DiskInfo)
            assert disk.total_space == 1000
            assert disk.used_space == 500
            assert disk.free_space == 500


def test_invalid_path():
    """Test handling of invalid paths."""
    analyzer = DiskAnalyzer()
    with pytest.raises(ValueError, match="Path does not exist"):
        analyzer.get_disk_usage("/nonexistent/path")
