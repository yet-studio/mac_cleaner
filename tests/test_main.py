import pytest
from unittest.mock import patch, MagicMock
import os
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from main import format_size, clean_system_paths, _create_path_size_map

def test_format_size():
    """Test size formatting function"""
    assert format_size(500) == "500.0 B"
    assert format_size(1024) == "1.0 KB"
    assert format_size(1024 * 1024) == "1.0 MB"
    assert format_size(1024 * 1024 * 1024) == "1.0 GB"
    assert format_size(1024 * 1024 * 1024 * 1024) == "1.0 TB"

@patch('main.get_system_paths')
@patch('main.FileCleaner')
def test_clean_system_paths_no_files(mock_cleaner, mock_get_paths, capsys):
    """Test cleaning when no files are found"""
    # Setup mock
    mock_get_paths.return_value = {
        'cache': [],
        'logs': []
    }
    
    # Run function
    clean_system_paths()
    
    # Check output
    captured = capsys.readouterr()
    assert "No cleanable directories found!" in captured.out

@patch('main.get_system_paths')
@patch('main.FileCleaner')
@patch('builtins.input')
@patch('os.access')
def test_clean_system_paths_with_files(mock_access, mock_input, mock_cleaner, mock_get_paths, capsys):
    """Test cleaning with files present"""
    # Setup mocks
    mock_get_paths.return_value = {
        'cache': [
            {'path': '/test/cache1', 'size': 1024},
            {'path': '/test/cache2', 'size': 2048}
        ],
        'logs': [
            {'path': '/test/log1', 'size': 512}
        ]
    }
    mock_input.return_value = 'y'
    mock_access.return_value = True  # Make all paths accessible
    
    cleaner_instance = MagicMock()
    cleaner_instance.clean_files.return_value = {
        'cleaned': ['/test/cache1', '/test/cache2'],
        'failed': []
    }
    mock_cleaner.return_value = cleaner_instance
    
    # Run function
    clean_system_paths()
    
    # Check output
    captured = capsys.readouterr()
    assert "cache" in captured.out.lower()
    assert "3.0 KB" in captured.out
    assert "Successfully cleaned" in captured.out

@patch('main.get_system_paths')
@patch('main.FileCleaner')
@patch('builtins.input')
@patch('os.access')
def test_clean_system_paths_user_cancels(mock_access, mock_input, mock_cleaner, mock_get_paths, capsys):
    """Test user cancellation of cleaning"""
    # Setup mocks
    mock_get_paths.return_value = {
        'cache': [{'path': '/test/cache1', 'size': 1024}]
    }
    mock_input.return_value = 'n'
    mock_access.return_value = True
    
    # Run function
    clean_system_paths()
    
    # Check output
    captured = capsys.readouterr()
    assert "Operation cancelled" in captured.out

@patch('main.get_system_paths')
@patch('main.FileCleaner')
@patch('builtins.input')
@patch('os.access')
def test_clean_system_paths_with_failures(mock_access, mock_input, mock_cleaner, mock_get_paths, capsys):
    """Test cleaning with some failures"""
    # Setup mocks
    mock_get_paths.return_value = {
        'cache': [
            {'path': '/test/cache1', 'size': 1024},
            {'path': '/test/cache2', 'size': 2048}
        ]
    }
    mock_input.return_value = 'y'
    mock_access.return_value = True
    
    cleaner_instance = MagicMock()
    cleaner_instance.clean_files.return_value = {
        'cleaned': ['/test/cache1'],
        'failed': [{'path': '/test/cache2', 'error': 'Operation not permitted'}]
    }
    mock_cleaner.return_value = cleaner_instance
    
    # Run function
    clean_system_paths()
    
    # Check output
    captured = capsys.readouterr()
    assert "Successfully cleaned 1 items" in captured.out
    assert "Permission denied for the following directories" in captured.out
    assert "/test/cache2" in captured.out

def test_create_path_size_map():
    """Test creating path size mapping"""
    paths = {
        'cache': [
            {'path': '/test/cache1', 'size': 1024},
            {'path': '/test/cache2', 'size': 2048}
        ],
        'logs': [
            {'path': '/test/log1', 'size': 512},
            {'path': '/test/log2'}  # Missing size
        ]
    }
    
    size_map = _create_path_size_map(paths)
    
    assert size_map == {
        '/test/cache1': 1024,
        '/test/cache2': 2048,
        '/test/log1': 512,
        '/test/log2': 0  # Default size for missing size
    }

def test_clean_system_paths_no_sudo(tmp_path, monkeypatch):
    """Test cleaning system paths without sudo"""
    # Mock os.geteuid to return non-root
    monkeypatch.setattr(os, 'geteuid', lambda: 1000)
    
    # Create test directories
    user_dir = tmp_path / "user_dir"
    system_dir = tmp_path / "system_dir"
    user_dir.mkdir()
    system_dir.mkdir()
    
    # Make user directory writable and system directory read-only
    os.chmod(str(user_dir), 0o755)
    os.chmod(str(system_dir), 0o555)
    
    # Create test files
    (user_dir / "test.txt").write_text("test")
    
    # Mock get_system_paths to return our test paths
    def mock_get_system_paths(with_size=False):
        return {
            "USER": [{"path": str(user_dir), "size": 4}],
            "SYSTEM": [{"path": str(system_dir), "size": 0}]  # Size 0 to skip this path
        }
    monkeypatch.setattr("main.get_system_paths", mock_get_system_paths)
    
    # Mock user input to confirm cleaning
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    
    # Mock os.access to allow access to user_dir but not system_dir
    def mock_access(path, mode):
        return path == str(user_dir)
    monkeypatch.setattr('os.access', mock_access)
    
    # Capture output
    from io import StringIO
    import sys
    output = StringIO()
    monkeypatch.setattr(sys, 'stdout', output)
    
    # Run the cleaning
    clean_system_paths()
    
    # Check output
    output_text = output.getvalue()
    assert "Successfully cleaned 1 items" in output_text
    
    # Check that only user directory was cleaned
    assert not user_dir.exists()
    assert system_dir.exists()
