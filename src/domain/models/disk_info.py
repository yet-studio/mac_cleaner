"""Models for disk information."""

from pydantic import BaseModel, computed_field


class DiskUsage(BaseModel):
    """Represents disk usage information."""

    total_bytes: int
    used_bytes: int
    free_bytes: int

    @computed_field
    def used_percentage(self) -> float:
        """Calculate the percentage of disk space used."""
        return (
            (self.used_bytes / self.total_bytes) * 100 if self.total_bytes > 0 else 0.0
        )


class DiskInfo(BaseModel):
    """Represents information about a disk."""

    path: str
    usage: DiskUsage
