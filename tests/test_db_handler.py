import pytest
from pathlib import Path
import json
from src.database.db_handler import DatabaseHandler
from unittest.mock import patch, mock_open

@pytest.fixture
def db_handler(tmp_path):
    """Create a DatabaseHandler instance with a temporary database path"""
    handler = DatabaseHandler()
    handler.db_path = tmp_path / 'test_locations_db.json'
    return handler

def test_ensure_db_exists(db_handler):
    """Test database creation with default data"""
    # Ensure database is created
    db_handler._ensure_db_exists()
    
    # Verify file exists
    assert db_handler.db_path.exists()
    
    # Verify content
    with open(db_handler.db_path) as f:
        data = json.load(f)
    
    assert 'locations' in data
    assert 'patterns' in data
    assert 'temp' in data['locations']
    assert 'logs' in data['locations']
    assert 'cache' in data['locations']

def test_load_data(db_handler):
    """Test loading data from database"""
    # Create test data
    test_data = {'test': 'data'}
    db_handler.db_path.parent.mkdir(parents=True, exist_ok=True)
    with open(db_handler.db_path, 'w') as f:
        json.dump(test_data, f)
    
    # Load and verify data
    loaded_data = db_handler.load_data()
    assert loaded_data == test_data

def test_load_data_nonexistent(db_handler):
    """Test loading from nonexistent database"""
    loaded_data = db_handler.load_data()
    assert loaded_data is None

def test_save_data(db_handler):
    """Test saving data to database"""
    test_data = {'test': 'data'}
    
    # Save data
    success = db_handler.save_data(test_data)
    assert success is True
    
    # Verify saved data
    with open(db_handler.db_path) as f:
        saved_data = json.load(f)
    assert saved_data == test_data

def test_save_data_error(db_handler, monkeypatch):
    """Test saving data with error"""
    def mock_open(*args, **kwargs):
        raise PermissionError("Access denied")
    
    monkeypatch.setattr('builtins.open', mock_open)
    success = db_handler.save_data({'test': 'data'})
    assert success is False

def test_get_locations(db_handler):
    """Test retrieving cleaning locations"""
    # Setup default database
    db_handler._ensure_db_exists()
    
    # Get locations
    locations = db_handler.get_locations()
    assert isinstance(locations, dict)
    assert 'temp' in locations
    assert 'logs' in locations
    assert 'cache' in locations
    assert all(isinstance(paths, list) for paths in locations.values())

def test_get_patterns(db_handler):
    """Test retrieving cleaning patterns"""
    # Setup default database
    db_handler._ensure_db_exists()
    
    # Get patterns
    patterns = db_handler.get_patterns()
    assert isinstance(patterns, dict)
    assert 'temp' in patterns
    assert 'logs' in patterns
    assert 'cache' in patterns
    assert all(isinstance(patterns_list, list) for patterns_list in patterns.values())

def test_add_location(db_handler):
    """Test adding new cleaning location"""
    # Setup default database
    db_handler._ensure_db_exists()
    
    # Add new location
    success = db_handler.add_location('test', '/test/path')
    assert success is True
    
    # Verify location was added
    locations = db_handler.get_locations()
    assert 'test' in locations
    assert '/test/path' in locations['test']

def test_add_pattern(db_handler):
    """Test adding new cleaning pattern"""
    # Setup default database
    db_handler._ensure_db_exists()
    
    # Add new pattern
    success = db_handler.add_pattern('test', '*.test')
    assert success is True
    
    # Verify pattern was added
    patterns = db_handler.get_patterns()
    assert 'test' in patterns
    assert '*.test' in patterns['test']

def test_add_location_nonexistent_category(db_handler):
    """Test adding location to nonexistent category"""
    result = db_handler.add_location('nonexistent', '/path/to/location')
    assert not result

def test_add_pattern_nonexistent_category(db_handler):
    """Test adding pattern to nonexistent category"""
    result = db_handler.add_pattern('nonexistent', '*.tmp')
    assert not result

def test_add_location_success(db_handler):
    """Test successfully adding location"""
    # Initialize with default data
    data = {
        'locations': {'temp': []},
        'patterns': {'temp': []}
    }
    db_handler.save_data(data)
    result = db_handler.add_location('temp', '/path/to/temp')
    assert result

def test_add_pattern_success(db_handler):
    """Test successfully adding pattern"""
    # Initialize with default data
    data = {
        'locations': {'temp': []},
        'patterns': {'temp': []}
    }
    db_handler.save_data(data)
    result = db_handler.add_pattern('temp', '*.tmp')
    assert result

def test_add_location_existing_category(db_handler):
    """Test adding location to existing category"""
    data = {
        'locations': {'temp': []},
        'patterns': {'temp': []}
    }
    db_handler.save_data(data)
    
    result = db_handler.add_location('temp', '/path/to/temp')
    assert result
    
    locations = db_handler.get_locations()
    assert 'temp' in locations
    assert '/path/to/temp' in locations['temp']

def test_add_pattern_existing_category(db_handler):
    """Test adding pattern to existing category"""
    data = {
        'locations': {'temp': []},
        'patterns': {'temp': []}
    }
    db_handler.save_data(data)
    
    result = db_handler.add_pattern('temp', '*.tmp')
    assert result
    
    patterns = db_handler.get_patterns()
    assert 'temp' in patterns
    assert '*.tmp' in patterns['temp']

def test_add_location_with_save(db_handler):
    """Test adding location with save"""
    data = {
        'locations': {'temp': []},
        'patterns': {'temp': []}
    }
    db_handler.save_data(data)
    
    result = db_handler.add_location('temp', '/path/to/temp')
    assert result
    
    # Verify that the location was saved
    loaded_data = db_handler.load_data()
    assert 'temp' in loaded_data['locations']
    assert '/path/to/temp' in loaded_data['locations']['temp']

def test_add_pattern_with_save(db_handler):
    """Test adding pattern with save"""
    data = {
        'locations': {'temp': []},
        'patterns': {'temp': []}
    }
    db_handler.save_data(data)
    
    result = db_handler.add_pattern('temp', '*.tmp')
    assert result
    
    # Verify that the pattern was saved
    loaded_data = db_handler.load_data()
    assert 'temp' in loaded_data['patterns']
    assert '*.tmp' in loaded_data['patterns']['temp']

def test_add_location_with_save_and_verify(db_handler):
    """Test adding location with save and verify"""
    data = {
        'locations': {'temp': []},
        'patterns': {'temp': []}
    }
    db_handler.save_data(data)
    
    # Add location and verify it was saved
    result = db_handler.add_location('temp', '/path/to/temp')
    assert result
    
    # Add another location to the same category
    result = db_handler.add_location('temp', '/path/to/another')
    assert result
    
    # Verify both locations were saved
    loaded_data = db_handler.load_data()
    assert 'temp' in loaded_data['locations']
    assert '/path/to/temp' in loaded_data['locations']['temp']
    assert '/path/to/another' in loaded_data['locations']['temp']

def test_add_pattern_with_save_and_verify(db_handler):
    """Test adding pattern with save and verify"""
    data = {
        'locations': {'temp': []},
        'patterns': {'temp': []}
    }
    db_handler.save_data(data)
    
    # Add pattern and verify it was saved
    result = db_handler.add_pattern('temp', '*.tmp')
    assert result
    
    # Add another pattern to the same category
    result = db_handler.add_pattern('temp', '*.temp')
    assert result
    
    # Verify both patterns were saved
    loaded_data = db_handler.load_data()
    assert 'temp' in loaded_data['patterns']
    assert '*.tmp' in loaded_data['patterns']['temp']
    assert '*.temp' in loaded_data['patterns']['temp']

def test_add_location_with_save_and_verify_existing(db_handler):
    """Test adding location with save and verify when category exists"""
    data = {
        'locations': {'temp': ['/path/to/temp']},
        'patterns': {'temp': []}
    }
    db_handler.save_data(data)
    
    # Add another location to the existing category
    result = db_handler.add_location('temp', '/path/to/another')
    assert result
    
    # Verify both locations were saved
    loaded_data = db_handler.load_data()
    assert 'temp' in loaded_data['locations']
    assert '/path/to/temp' in loaded_data['locations']['temp']
    assert '/path/to/another' in loaded_data['locations']['temp']

def test_add_pattern_with_save_and_verify_existing(db_handler):
    """Test adding pattern with save and verify when category exists"""
    data = {
        'locations': {'temp': []},
        'patterns': {'temp': ['*.tmp']}
    }
    db_handler.save_data(data)
    
    # Add another pattern to the existing category
    result = db_handler.add_pattern('temp', '*.temp')
    assert result
    
    # Verify both patterns were saved
    loaded_data = db_handler.load_data()
    assert 'temp' in loaded_data['patterns']
    assert '*.tmp' in loaded_data['patterns']['temp']
    assert '*.temp' in loaded_data['patterns']['temp']

def test_add_location_duplicate(db_handler):
    """Test adding duplicate location"""
    test_data = {
        'locations': {'test': ['/test/path']},
        'patterns': {'test': ['*.tmp']}
    }
    
    with patch('pathlib.Path.exists', return_value=True):
        with patch('json.load', return_value=test_data):
            with patch('builtins.open', mock_open()):
                result = db_handler.add_location('test', '/test/path')
                assert result is True

def test_add_pattern_duplicate(db_handler):
    """Test adding duplicate pattern"""
    test_data = {
        'locations': {'test': ['/test/path']},
        'patterns': {'test': ['*.tmp']}
    }
    
    with patch('pathlib.Path.exists', return_value=True):
        with patch('json.load', return_value=test_data):
            with patch('builtins.open', mock_open()):
                result = db_handler.add_pattern('test', '*.tmp')
                assert result is True
