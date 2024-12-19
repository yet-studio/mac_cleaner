"""Memory analyzer service."""

from typing import List

import psutil

from src.domain.models.memory_info import MemoryInfo, ProcessMemoryInfo


class MemoryAnalyzer:
    """Service for analyzing system and process memory usage."""

    def get_memory_usage(self) -> MemoryInfo:
        """Get system memory usage information.

        Returns:
            MemoryInfo: System memory usage information.
        """
        memory = psutil.virtual_memory()
        return MemoryInfo(
            total_bytes=memory.total,
            available_bytes=memory.available,
            used_bytes=memory.used,
            used_percent=memory.percent,
        )

    def get_process_memory(self, pid: int) -> ProcessMemoryInfo:
        """Get memory usage information for a specific process.

        Args:
            pid: Process ID to analyze.

        Returns:
            ProcessMemoryInfo: Process memory usage information.

        Raises:
            ValueError: If the process ID is invalid or process not found.
        """
        try:
            process = psutil.Process(pid)
            memory_info = process.memory_info()
            process_name = process.name()  # Call name() once and store result
            memory_percent = process.memory_percent()  # Call memory_percent() once
            return ProcessMemoryInfo(
                pid=process.pid,
                name=process_name,
                memory_percent=memory_percent,
                rss_bytes=memory_info.rss,
                vms_bytes=memory_info.vms,
            )
        except psutil.NoSuchProcess as exc:
            raise ValueError(f"Process with ID {pid} not found") from exc

    def get_top_memory_processes(self, limit: int = 5) -> List[ProcessMemoryInfo]:
        """Get list of top memory-consuming processes.

        Args:
            limit: Maximum number of processes to return (default: 5).

        Returns:
            List[ProcessMemoryInfo]: List of process memory information, sorted by memory usage.
        """
        processes = []
        for proc in psutil.process_iter():
            try:
                memory_info = proc.memory_info()
                process_name = proc.name()  # Call name() once and store result
                memory_percent = proc.memory_percent()  # Call memory_percent() once
                processes.append(
                    ProcessMemoryInfo(
                        pid=proc.pid,
                        name=process_name,
                        memory_percent=memory_percent,
                        rss_bytes=memory_info.rss,
                        vms_bytes=memory_info.vms,
                    )
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Sort by memory percentage in descending order
        processes.sort(key=lambda x: x.memory_percent, reverse=True)
        return processes[:limit]
