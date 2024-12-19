from dataclasses import dataclass
from pathlib import Path
from typing import List
import os

@dataclass
class ValidationResult:
    """Result of path validation"""
    is_valid: bool
    error_message: str = ""
    requires_sudo: bool = False

class PathValidator:
    """Validates paths for safe file operations"""

    def __init__(self, protected_paths: List[str]):
        """Initialize validator with protected paths"""
        if not isinstance(protected_paths, list):
            raise TypeError("protected_paths must be a list")
            
        # Validate all paths are absolute
        for path in protected_paths:
            if not os.path.isabs(path):
                raise ValueError(f"Protected path must be absolute: {path}")
                
        self.protected_paths = [Path(p) for p in protected_paths]

    def validate_paths(self, paths: List[Path]) -> List[ValidationResult]:
        """Validate multiple paths"""
        if not paths:
            return []
        return [self.validate_path(p) for p in paths]

    def validate_path(self, path: Path) -> ValidationResult:
        """Validate a single path"""
        if path is None:
            raise TypeError("Path cannot be None")
            
        try:
            # Check if path exists
            if not path.exists():
                return ValidationResult(
                    is_valid=False,
                    error_message="Path does not exist"
                )

            # Resolve the real path (follow symlinks)
            real_path = path.resolve()

            # Check if path is protected
            if self.is_path_protected(real_path):
                return ValidationResult(
                    is_valid=False,
                    error_message=f"Protected system path: {real_path}"
                )

            # Check if path requires elevated privileges
            requires_sudo = os.stat(str(path)).st_uid == 0

            return ValidationResult(
                is_valid=True,
                requires_sudo=requires_sudo
            )

        except PermissionError:
            return ValidationResult(
                is_valid=False,
                error_message="Permission denied",
                requires_sudo=True
            )
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error_message=str(e)
            )

    def is_path_protected(self, path: Path) -> bool:
        """Check if path is protected"""
        try:
            real_path = path.resolve()
            return any(
                str(real_path).startswith(str(p))
                for p in self.protected_paths
            )
        except Exception:
            # If we can't resolve the path, consider it protected
            return True