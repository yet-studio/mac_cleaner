import pytest
from pathlib import Path
from src.core.scanner import FileScanner
from unittest.mock import patch, MagicMock

@pytest.fixture
def scanner():
    return FileScanner()

@pytest.fixture
def mock_db_handler():
    handler = MagicMock()
    handler.get_patterns.return_value = {
        'temp': ['*.tmp', '*.temp'],
        'logs': ['*.log']
    }
    return handler

def test_get_file_type(scanner):
    """Test file type detection"""
    # Test log files
    assert scanner._get_file_type(Path('test.log')) == 'log'
    assert scanner._get_file_type(Path('test.txt')) == 'log'
    
    # Test temp files
    assert scanner._get_file_type(Path('test.tmp')) == 'temp'
    assert scanner._get_file_type(Path('test.temp')) == 'temp'
    
    # Test cache files
    with patch.object(Path, 'parent') as mock_parent:
        mock_parent.name = 'cache'
        assert scanner._get_file_type(Path('test.file')) == 'cache'
    
    # Test other files
    assert scanner._get_file_type(Path('test.other')) == 'other'

def test_scan_directory(scanner, tmp_path):
    """Test directory scanning"""
    # Create test files
    test_files = [
        tmp_path / 'test.log',
        tmp_path / 'test.tmp',
        tmp_path / 'cache' / 'test.file'
    ]
    
    # Create test directory structure
    (tmp_path / 'cache').mkdir()
    for file in test_files:
        file.parent.mkdir(exist_ok=True)
        file.touch()
    
    # Scan directory
    results = scanner.scan_directory(tmp_path)
    
    # Verify results
    assert len(results) == len(test_files)
    for result in results:
        assert isinstance(result, dict)
        assert 'path' in result
        assert 'size' in result
        assert 'modified' in result
        assert 'type' in result

def test_scan_directory_error(scanner):
    """Test scanning nonexistent directory"""
    results = scanner.scan_directory('/nonexistent/path')
    assert len(results) == 0

def test_scan_directory_with_patterns(scanner, mock_db_handler, tmp_path):
    """Test scanning with specific patterns"""
    scanner.db_handler = mock_db_handler
    
    # Create test files
    test_files = [
        tmp_path / 'test1.tmp',
        tmp_path / 'test2.log',
        tmp_path / 'test3.other'
    ]
    for file in test_files:
        file.touch()
    
    # Scan for temp files
    results = scanner.scan_directory(tmp_path, file_type='temp')
    assert len(results) == 1
    assert results[0]['path'].endswith('.tmp')

def test_get_system_paths(scanner):
    """Test system paths retrieval"""
    paths = scanner.get_system_paths()
    assert isinstance(paths, dict)
    assert 'temp' in paths
    assert 'logs' in paths
    assert all(isinstance(path_list, list) for path_list in paths.values())
    assert all(isinstance(path, str) for path_list in paths.values() for path in path_list)

def test_scan_multiple_directories(scanner, tmp_path):
    """Test scanning multiple directories"""
    # Create test directories and files
    dir1 = tmp_path / 'dir1'
    dir2 = tmp_path / 'dir2'
    dir1.mkdir()
    dir2.mkdir()
    
    (dir1 / 'test1.tmp').touch()
    (dir2 / 'test2.tmp').touch()
    
    # Scan directories
    results = scanner.scan_multiple_directories([dir1, dir2])
    assert len(results) == 2
    assert all('path' in result for result in results)

def test_scan_with_size_filter(scanner, tmp_path):
    """Test scanning with size filter"""
    test_file = tmp_path / 'test.tmp'
    test_file.write_bytes(b'0' * 1024)  # 1KB file
    
    # Scan with min size filter
    results = scanner.scan_directory(tmp_path, min_size=2048)  # 2KB
    assert len(results) == 0
    
    # Scan with max size filter
    results = scanner.scan_directory(tmp_path, max_size=512)  # 512B
    assert len(results) == 0
    
    # Scan with matching size filter
    results = scanner.scan_directory(tmp_path, min_size=512, max_size=2048)
    assert len(results) == 1

def test_scan_directory_with_general_error(scanner, tmp_path):
    """Test scan_directory with a general error"""
    test_file = tmp_path / 'test.txt'
    test_file.touch()
    
    with patch('pathlib.Path.glob', side_effect=Exception('Unknown error')):
        files = scanner.scan_directory(tmp_path)
        assert len(files) == 0