import pytest
from pathlib import Path
from src.core.validator import PathValidator, ValidationResult, ValidationError

def test_validator_rejects_protected_paths():
    validator = PathValidator(["/System", "/usr/bin"])
    result = validator.validate_path(Path("/System/Library/something"))
    assert not result.is_valid
    assert "Protected system path" in result.error_message

def test_validator_accepts_safe_paths():
    validator = PathValidator(["/System"])
    result = validator.validate_path(Path("/Users/test/Documents/file.txt"))
    assert result.is_valid
    assert result.error_message == ""

def test_validator_resolves_symlinks():
    with pytest.fixture_path("/tmp/test_symlink") as symlink_path:
        symlink_path.symlink_to("/System/test")
        validator = PathValidator(["/System"])
        result = validator.validate_path(symlink_path)
        assert not result.is_valid
        assert "Protected system path" in result.error_message

def test_validator_handles_nonexistent_paths():
    validator = PathValidator(["/System"])
    result = validator.validate_path(Path("/nonexistent/path"))
    assert not result.is_valid
    assert "Path does not exist" in result.error_message

def test_validator_prevents_parent_directory_traversal():
    validator = PathValidator(["/System"])
    result = validator.validate_path(Path("/Users/../System/Library"))
    assert not result.is_valid
    assert "Path traversal detected" in result.error_message

def test_validator_checks_path_permissions():
    validator = PathValidator(["/System"])
    result = validator.validate_path(Path("/Users"))
    assert result.requires_sudo == Path("/Users").stat().st_uid == 0

def test_validator_batch_validation():
    validator = PathValidator(["/System"])
    paths = [
        Path("/Users/test/file.txt"),
        Path("/System/file"),
        Path("/tmp/test")
    ]
    results = validator.validate_paths(paths)
    assert len(results) == 3
    assert any(not r.is_valid for r in results)
    assert any(r.is_valid for r in results) 