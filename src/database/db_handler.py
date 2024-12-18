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
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.db_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            self.logger.error(f"Error saving database: {e}")
            return False
    
    def get_locations(self) -> Dict[str, List[str]]:
        """Get cleaning locations"""
        data = self.load_data()
        return data.get('locations', {}) if data else {}
    
    def get_patterns(self) -> Dict[str, List[str]]:
        """Get cleaning patterns"""
        data = self.load_data()
        return data.get('patterns', {}) if data else {}
    
    def add_location(self, category: str, path: str) -> bool:
        """Add new cleaning location"""
        data = self.load_data()
        if not data:
            return False
        
        if category not in data['locations']:
            data['locations'][category] = []
        
        if path not in data['locations'][category]:
            data['locations'][category].append(path)
            return self.save_data(data)
        return True
    
    def add_pattern(self, category: str, pattern: str) -> bool:
        """Add new cleaning pattern"""
        data = self.load_data()
        if not data:
            return False
        
        if category not in data['patterns']:
            data['patterns'][category] = []
        
        if pattern not in data['patterns'][category]:
            data['patterns'][category].append(pattern)
            return self.save_data(data)
        return True