import json
from pathlib import Path
from typing import Dict, List, Optional
import logging

class DatabaseHandler:
    """Handle database operations for cleaning locations and patterns"""
    
    def __init__(self):
        self.db_path = Path('config/locations_db.json')
        self.logger = logging.getLogger(__name__)
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database if it doesn't exist"""
        if not self.db_path.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            default_data = {
                'locations': {
                    'temp': [
                        '~/Library/Caches',
                        '/tmp',
                        '/var/tmp'
                    ],
                    'logs': [
                        '~/Library/Logs',
                        '/var/log'
                    ],
                    'cache': [
                        '~/Library/Caches',
                        '~/Library/Application Support/*/Cache'
                    ]
                },
                'patterns': {
                    'temp': ['*.tmp', '*.temp', 'Temp*'],
                    'logs': ['*.log', '*.txt'],
                    'cache': ['Cache*', '*.cache']
                }
            }
            self.save_data(default_data)
    
    def load_data(self) -> Optional[Dict]:
        """Load database content"""
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading database: {e}")
            return None
    
    def save_data(self, data: Dict) -> bool:
        """Save data to database"""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            self.logger.error(f"Error saving to database: {e}")
            return False
    
    def get_locations(self, location_type: Optional[str] = None) -> Dict[str, List[str]]:
        """Get cleaning locations"""
        data = self.load_data()
        if not data:
            return {}
        
        locations = data.get('locations', {})
        if location_type:
            return {location_type: locations.get(location_type, [])}
        return locations
    
    def get_patterns(self, pattern_type: Optional[str] = None) -> Dict[str, List[str]]:
        """Get cleaning patterns"""
        data = self.load_data()
        if not data:
            return {}
        
        patterns = data.get('patterns', {})
        if pattern_type:
            return {pattern_type: patterns.get(pattern_type, [])}
        return patterns
    
    def add_location(self, location_type: str, path: str) -> bool:
        """Add new location to database"""
        data = self.load_data()
        if not data:
            return False
        
        if location_type not in data['locations']:
            data['locations'][location_type] = []
        
        if path not in data['locations'][location_type]:
            data['locations'][location_type].append(path)
            return self.save_data(data)
        return True
    
    def add_pattern(self, pattern_type: str, pattern: str) -> bool:
        """Add new pattern to database"""
        data = self.load_data()
        if not data:
            return False
        
        if pattern_type not in data['patterns']:
            data['patterns'][pattern_type] = []
        
        if pattern not in data['patterns'][pattern_type]:
            data['patterns'][pattern_type].append(pattern)
            return self.save_data(data)
        return True