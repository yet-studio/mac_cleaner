"""Service for analyzing disk space."""

from typing import List

import psutil

from ..models.disk_info import DiskInfo, DiskUsage


class DiskAnalyzer:
    """Service for analyzing disk space usage."""

    def get_disk_usage(self, path: str) -> DiskInfo:
        """
        Get disk usage information for a specific path.

        Args:
            path: The path to analyze

        Returns:
            DiskInfo object containing usage information

        Raises:
            ValueError: If the path is invalid or inaccessible
        """
        try:
            usage = psutil.disk_usage(path)
            return DiskInfo(
                path=path,
                usage=DiskUsage(
                    total_bytes=usage.total,
                    used_bytes=usage.used,
                    free_bytes=usage.free,
                ),
            )
        except (FileNotFoundError, PermissionError) as e:
            raise ValueError(f"Invalid disk path: {path}") from e

    def get_all_disks(self) -> List[DiskInfo]:
        """
        Get disk usage information for all mounted disks.

        Returns:
            List of DiskInfo objects for all mounted disks
        """
        partitions = psutil.disk_partitions()
        return [self.get_disk_usage(partition.mountpoint) for partition in partitions]
