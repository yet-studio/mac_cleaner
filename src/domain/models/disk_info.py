"""Disk information models."""

from dataclasses import dataclass


@dataclass
class DiskInfo:
    """Information about disk usage."""

    path: str
    total_space: int
    used_space: int
    free_space: int

    @property
    def used_percentage(self) -> float:
        """Calculate the percentage of disk space used."""
        return (
            (self.used_space / self.total_space) * 100 if self.total_space > 0 else 0.0
        )
