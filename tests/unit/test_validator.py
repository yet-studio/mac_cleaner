import pytest
from pathlib import Path
from src.core.validator import PathValidator, ValidationResult
from unittest.mock import Mock, patch

def test_validator_rejects_protected_paths():
    validator = PathValidator(["/System"])
    result = validator.validate_path(Path("/System/Library"))
    assert not result.is_valid
    assert "Protected system path" in result.error_message

def test_validator_accepts_safe_paths(tmp_path):
    validator = PathValidator(["/System"])
    test_file = tmp_path / "test.txt"
    test_file.touch()
    result = validator.validate_path(test_file)
    assert result.is_valid
    assert result.error_message == ""

def test_validator_handles_nonexistent_paths():
    validator = PathValidator(["/System"])
    result = validator.validate_path(Path("/nonexistent/path"))
    assert not result.is_valid
    assert "Path does not exist" in result.error_message

def test_validator_with_empty_protected_paths(tmp_path):
    validator = PathValidator([])
    test_file = tmp_path / "test.txt"
    test_file.touch()
    result = validator.validate_path(test_file)
    assert result.is_valid

def test_validator_with_relative_protected_paths():
    with pytest.raises(ValueError):
        PathValidator(["relative/path"])

def test_validate_paths_empty_list():
    validator = PathValidator(["/System"])
    results = validator.validate_paths([])
    assert results == []

def test_validator_with_none_path():
    validator = PathValidator(["/System"])
    with pytest.raises(TypeError):
        validator.validate_path(None)

def test_validator_handles_permission_error():
    validator = PathValidator(["/System"])
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.resolve.side_effect = PermissionError("Permission denied")
    
    result = validator.validate_path(mock_path)
    assert not result.is_valid
    assert "Permission denied" in result.error_message
    assert result.requires_sudo

def test_is_path_protected_with_exception():
    validator = PathValidator(["/System"])
    mock_path = Mock(spec=Path)
    mock_path.resolve.side_effect = OSError("Cannot resolve")
    assert validator.is_path_protected(mock_path) is True

def test_validator_batch_validation(tmp_path):
    validator = PathValidator(["/System"])
    
    # Create test files
    safe_file = tmp_path / "safe.txt"
    safe_file.touch()
    
    paths = [
        safe_file,
        Path("/System/file"),
        Path("/nonexistent/path")
    ]
    
    results = validator.validate_paths(paths)
    assert len(results) == 3
    assert results[0].is_valid  # safe file
    assert not results[1].is_valid  # protected path
    assert not results[2].is_valid  # nonexistent path