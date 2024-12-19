"""Memory information models."""

from pydantic import BaseModel, Field


class MemoryInfo(BaseModel):
    """System memory information model."""

    total_bytes: int = Field(..., description="Total physical memory in bytes")
    available_bytes: int = Field(..., description="Available memory in bytes")
    used_bytes: int = Field(..., description="Used memory in bytes")
    used_percent: float = Field(..., description="Memory usage percentage")


class ProcessMemoryInfo(BaseModel):
    """Process memory information model."""

    pid: int = Field(..., description="Process ID")
    name: str = Field(..., description="Process name")
    memory_percent: float = Field(..., description="Process memory usage percentage")
    rss_bytes: int = Field(
        ..., description="Resident Set Size (RSS) - physical memory used by process"
    )
    vms_bytes: int = Field(
        ..., description="Virtual Memory Size (VMS) - virtual memory used by process"
    )
