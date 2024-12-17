from pathlib import Path
from typing import List, Dict, Optional
import os
import logging

class FileScanner:
    """Scanner for identifying files to clean"""
    
    def __init__(self, db_handler=None):
        self.db_handler = db_handler
        self.logger = logging.getLogger(__name__)
    
    def scan_directory(self, directory: Path) -> List[Dict]:
        """Scan a directory for files"""
        files = []
        try:
            directory = Path(directory).expanduser()
            if directory.exists():
                for item in directory.rglob('*'):
                    if item.is_file():
                        files.append({
                            'path': str(item),
                            'size': item.stat().st_size,
                            'modified': item.stat().st_mtime,
                            'type': self._get_file_type(item)
                        })
        except Exception as e:
            self.logger.error(f"Error scanning {directory}: {e}")
        return files
    
    def _get_file_type(self, file_path: Path) -> str:
        """Determine file type"""
        if file_path.suffix.lower() in ['.log', '.txt']:
            return 'log'
        elif file_path.suffix.lower() in ['.tmp', '.temp']:
            return 'temp'
        elif file_path.parent.name.lower() in ['cache', 'caches']:
            return 'cache'
        return 'other'
    
    def get_system_paths(self) -> Dict[str, List[str]]:
        """Get system paths to scan"""
        return {
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
        }
    
    def scan_system(self, scan_types: Optional[List[str]] = None) -> Dict[str, List[Dict]]:
        """Scan system for files to clean"""
        if scan_types is None:
            scan_types = ['temp', 'logs', 'cache']
        
        results = {}
        paths = self.get_system_paths()
        
        for scan_type in scan_types:
            if scan_type in paths:
                results[scan_type] = []
                for directory in paths[scan_type]:
                    files = self.scan_directory(Path(directory))
                    results[scan_type].extend(files)
        
        return results