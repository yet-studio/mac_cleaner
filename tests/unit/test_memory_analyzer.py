"""Unit tests for memory analyzer."""

from typing import Dict
from unittest.mock import Mock, patch

import psutil
import pytest
from pydantic import BaseModel

from src.domain.models.memory_info import MemoryInfo, ProcessMemoryInfo
from src.domain.services.memory_analyzer import MemoryAnalyzer


class TestMemoryAnalyzer:
    """Test suite for MemoryAnalyzer class."""

    @pytest.fixture
    def memory_analyzer(self) -> MemoryAnalyzer:
        """Fixture for MemoryAnalyzer instance."""
        return MemoryAnalyzer()

    @pytest.fixture
    def mock_memory_info(self) -> Dict[str, int]:
        """Mock system memory data."""
        return {
            "total": 16 * 1024 * 1024 * 1024,  # 16 GB
            "available": 8 * 1024 * 1024 * 1024,  # 8 GB
            "used": 8 * 1024 * 1024 * 1024,  # 8 GB
            "percent": 50.0,
        }

    @pytest.fixture
    def mock_process_info(self) -> Dict[str, int]:
        """Mock process memory data."""
        return {
            "pid": 1234,
            "name": "test_process",
            "memory_percent": 5.0,
            "memory_info": Mock(
                rss=512 * 1024 * 1024,  # 512 MB RSS
                vms=1024 * 1024 * 1024,  # 1 GB VMS
            ),
        }

    def test_memory_info_model(self):
        """Test MemoryInfo model validation."""
        memory_info = MemoryInfo(
            total_bytes=16 * 1024 * 1024 * 1024,
            available_bytes=8 * 1024 * 1024 * 1024,
            used_bytes=8 * 1024 * 1024 * 1024,
            used_percent=50.0,
        )
        assert isinstance(memory_info, BaseModel)
        assert memory_info.used_percent == 50.0

    def test_process_memory_info_model(self):
        """Test ProcessMemoryInfo model validation."""
        process_info = ProcessMemoryInfo(
            pid=1234,
            name="test_process",
            memory_percent=5.0,
            rss_bytes=512 * 1024 * 1024,
            vms_bytes=1024 * 1024 * 1024,
        )
        assert isinstance(process_info, BaseModel)
        assert process_info.memory_percent == 5.0

    @patch("psutil.virtual_memory")
    def test_get_memory_usage(
        self, mock_virtual_memory, memory_analyzer, mock_memory_info
    ):
        """Test getting system memory usage information."""
        mock_virtual_memory.return_value = Mock(
            total=mock_memory_info["total"],
            available=mock_memory_info["available"],
            used=mock_memory_info["used"],
            percent=mock_memory_info["percent"],
        )

        memory_info = memory_analyzer.get_memory_usage()

        assert isinstance(memory_info, MemoryInfo)
        assert memory_info.total_bytes == mock_memory_info["total"]
        assert memory_info.available_bytes == mock_memory_info["available"]
        assert memory_info.used_bytes == mock_memory_info["used"]
        assert memory_info.used_percent == mock_memory_info["percent"]

    @patch("psutil.Process")
    def test_get_process_memory(
        self, mock_process_class, memory_analyzer, mock_process_info
    ):
        """Test getting memory usage for a specific process."""
        mock_process = Mock()
        mock_process.pid = mock_process_info["pid"]
        mock_process.name.return_value = mock_process_info["name"]
        mock_process.memory_percent.return_value = mock_process_info["memory_percent"]
        mock_process.memory_info.return_value = mock_process_info["memory_info"]
        mock_process_class.return_value = mock_process

        process_info = memory_analyzer.get_process_memory(mock_process_info["pid"])

        assert isinstance(process_info, ProcessMemoryInfo)
        assert process_info.pid == mock_process_info["pid"]
        assert process_info.name == mock_process_info["name"]
        assert process_info.memory_percent == mock_process_info["memory_percent"]
        assert process_info.rss_bytes == mock_process_info["memory_info"].rss
        assert process_info.vms_bytes == mock_process_info["memory_info"].vms

    @patch("psutil.Process")
    def test_invalid_process_id(self, mock_process_class, memory_analyzer):
        """Test handling of invalid process ID."""
        mock_process_class.side_effect = psutil.NoSuchProcess(1234)

        with pytest.raises(ValueError, match="Process with ID 1234 not found"):
            memory_analyzer.get_process_memory(1234)

    @patch("psutil.process_iter")
    def test_get_top_memory_processes(
        self, mock_process_iter, memory_analyzer, mock_process_info
    ):
        """Test getting top memory-consuming processes."""
        mock_process = Mock()
        mock_process.pid = mock_process_info["pid"]
        mock_process.name.return_value = mock_process_info["name"]
        mock_process.memory_percent.return_value = mock_process_info["memory_percent"]
        mock_process.memory_info.return_value = mock_process_info["memory_info"]
        mock_process_iter.return_value = [mock_process]

        top_processes = memory_analyzer.get_top_memory_processes(limit=5)

        assert len(top_processes) <= 5
        assert isinstance(top_processes[0], ProcessMemoryInfo)
        assert top_processes[0].pid == mock_process_info["pid"]
        assert top_processes[0].name == mock_process_info["name"]
        assert top_processes[0].memory_percent == mock_process_info["memory_percent"]

    @patch("psutil.process_iter")
    def test_get_top_memory_processes_with_errors(
        self, mock_process_iter, memory_analyzer, mock_process_info
    ):
        """Test getting top memory-consuming processes with some processes raising errors."""
        # Create one good process and one that raises an error
        good_process = Mock()
        good_process.pid = mock_process_info["pid"]
        good_process.name.return_value = mock_process_info["name"]
        good_process.memory_percent.return_value = mock_process_info["memory_percent"]
        good_process.memory_info.return_value = mock_process_info["memory_info"]

        error_process = Mock()
        error_process.memory_info.side_effect = psutil.NoSuchProcess(9999)

        mock_process_iter.return_value = [good_process, error_process]

        top_processes = memory_analyzer.get_top_memory_processes(limit=5)

        assert len(top_processes) == 1  # Only the good process should be included
        assert isinstance(top_processes[0], ProcessMemoryInfo)
        assert top_processes[0].pid == mock_process_info["pid"]
        assert top_processes[0].name == mock_process_info["name"]
        assert top_processes[0].memory_percent == mock_process_info["memory_percent"]
