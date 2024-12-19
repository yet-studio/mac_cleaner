"""Disk analyzer service for analyzing disk usage."""

import os
import shutil
from typing import List

from ..models.disk_info import DiskInfo


class DiskAnalyzer:
    """Service for analyzing disk usage."""

    def get_disk_usage(self, path: str) -> DiskInfo:
        """Get disk usage information for a given path."""
        try:
            if not os.path.exists(path):
                raise ValueError(f"Path does not exist: {path}")

            if not os.access(path, os.R_OK):
                raise PermissionError(f"Permission denied: {path}")

            total, used, free = shutil.disk_usage(path)
            return DiskInfo(
                path=path,
                total_space=total,
                used_space=used,
                free_space=free,
            )
        except Exception as e:
            raise ValueError(f"Error getting disk usage for {path}: {str(e)}") from e

    def get_all_disks(self) -> List[DiskInfo]:
        """Get disk usage information for all mounted disks."""
        try:
            disks = []
            for path in self._get_mount_points():
                if os.path.exists(path):
                    disks.append(self.get_disk_usage(path))
            return disks
        except Exception as e:
            raise ValueError(f"Error getting all disks: {str(e)}") from e

    def _get_mount_points(self) -> List[str]:
        """Get all mount points."""
        return ["/", "/home"]  # For now, just return root and home. Expand later.
