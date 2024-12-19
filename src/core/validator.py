from dataclasses import dataclass
from pathlib import Path
from typing import List, Set
import os

@dataclass
class ValidationResult:
    """Result of path validation"""
    is_valid: bool
    error_message: str = ""
    requires_sudo: bool = False

class ValidationError(Exception):
    """Raised when path validation fails"""
    pass

class PathValidator:
    """Validates paths for safe file operations"""

    def __init__(self, protected_paths: List[str]):
        """Initialize validator with protected paths
        
        Args:
            protected_paths: List of absolute paths that should not be modified
        """
        self.protected_paths = {Path(p).resolve() for p in protected_paths}

    def validate_paths(self, paths: List[Path]) -> List[ValidationResult]:
        """Validate multiple paths
        
        Args:
            paths: List of paths to validate
            
        Returns:
            List of validation results for each path
        """
        return [self.validate_path(p) for p in paths]

    def validate_path(self, path: Path) -> ValidationResult:
        """Validate a single path
        
        Args:
            path: Path to validate
            
        Returns:
            ValidationResult indicating if path is safe to operate on
        """
        try:
            # Check if path exists
            if not path.exists():
                return ValidationResult(
                    is_valid=False,
                    error_message="Path does not exist"
                )

            # Resolve the real path (follow symlinks)
            real_path = path.resolve()

            # Check for path traversal attempts
            if '..' in str(real_path):
                return ValidationResult(
                    is_valid=False,
                    error_message="Path traversal detected"
                )

            # Check if path is in protected paths
            for protected in self.protected_paths:
                if str(real_path).startswith(str(protected)):
                    return ValidationResult(
                        is_valid=False,
                        error_message=f"Protected system path: {protected}"
                    )

            # Check if path requires elevated privileges
            requires_sudo = path.stat().st_uid == 0

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
                error_message=f"Validation error: {str(e)}"
            )

    def is_path_protected(self, path: Path) -> bool:
        """Check if path is protected
        
        Args:
            path: Path to check
            
        Returns:
            True if path is protected, False otherwise
        """
        try:
            real_path = path.resolve()
            return any(
                str(real_path).startswith(str(p))
                for p in self.protected_paths
            )
        except Exception:
            # If we can't resolve the path, consider it protected
            return True 