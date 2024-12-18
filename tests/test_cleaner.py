import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.core.cleaner import FileCleaner

@pytest.fixture
def cleaner():
    return FileCleaner()

def test_clean_files_basic(cleaner, tmp_path):
    """Test basic file cleaning functionality"""
    test_file = tmp_path / 'test.txt'
    test_file.touch()
    
    files = [{'path': str(test_file)}]
    results = cleaner.clean_files(files)
    
    assert len(results['cleaned']) == 1
    assert not test_file.exists()

def test_clean_files_nonexistent(cleaner):
    """Test cleaning nonexistent file"""
    files = [{'path': '/nonexistent/file.txt'}]
    results = cleaner.clean_files(files)
    
    assert len(results['failed']) == 1
    assert 'does not exist' in results['failed'][0]['error']

def test_clean_files_invalid_input(cleaner):
    """Test clean_files with invalid input"""
    with pytest.raises(ValueError):
        cleaner.clean_files("not a list")

def test_clean_files_error(cleaner, tmp_path):
    """Test clean_files with error"""
    test_file = tmp_path / 'test.txt'
    test_file.touch()
    
    files = [{'path': str(test_file)}]
    with patch('pathlib.Path.unlink', side_effect=Exception('Test error')):
        results = cleaner.clean_files(files)
        assert len(results['failed']) == 1
        assert 'Test error' in results['failed'][0]['error']

def test_clean_by_pattern_basic(cleaner, tmp_path):
    """Test basic pattern cleaning"""
    test_file = tmp_path / 'test.tmp'
    test_file.touch()
    
    results = cleaner.clean_by_pattern(tmp_path, ['*.tmp'])
    
    assert len(results['cleaned']) == 1
    assert not test_file.exists()

def test_clean_by_pattern_nonexistent_dir(cleaner):
    """Test clean_by_pattern with nonexistent directory"""
    results = cleaner.clean_by_pattern('/nonexistent/dir', ['*.tmp'])
    
    assert len(results['failed']) == 1
    assert 'Directory does not exist' in results['failed'][0]['error']

def test_clean_by_pattern_error(cleaner, tmp_path):
    """Test clean_by_pattern with error"""
    test_file = tmp_path / 'test.tmp'
    test_file.touch()
    
    with patch('pathlib.Path.unlink', side_effect=Exception('Test error')):
        results = cleaner.clean_by_pattern(tmp_path, ['*.tmp'])
        assert len(results['failed']) == 1
        assert 'Test error' in results['failed'][0]['error']

def test_clean_by_pattern_access_error(cleaner, tmp_path):
    """Test clean_by_pattern with directory access error"""
    with patch('os.walk', side_effect=Exception('Access error')):
        results = cleaner.clean_by_pattern(tmp_path, ['*.tmp'])
        assert len(results['failed']) == 1
        assert 'Access error' in results['failed'][0]['error']

def test_estimate_space_saving(cleaner):
    """Test space saving estimation"""
    files = [
        {'path': 'file1.txt', 'size': 100},
        {'path': 'file2.txt', 'size': 200}
    ]
    assert cleaner.estimate_space_saving(files) == 300