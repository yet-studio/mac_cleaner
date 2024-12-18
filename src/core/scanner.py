from pathlib import Path
from typing import List, Dict, Optional
import logging

class FileScanner:
    """Scanner for identifying files to clean"""
    
    def __init__(self, db_handler=None):
        self.db_handler = db_handler
        self.logger = logging.getLogger(__name__)
    
    def _get_file_type(self, file_path: Path) -> str:
        """Determine file type"""
        if file_path.suffix.lower() in ['.log', '.txt']:
            return 'log'
        elif file_path.suffix.lower() in ['.tmp', '.temp']:
            return 'temp'
        elif file_path.parent.name.lower() in ['cache', 'caches']:
            return 'cache'
        return 'other'
    
    def scan_directory(self, directory: Path, file_type: Optional[str] = None,
                      min_size: Optional[int] = None, max_size: Optional[int] = None) -> List[Dict]:
        """Scan a directory for files"""
        files = []
        try:
            directory = Path(directory).expanduser()
            if directory.exists():
                patterns = None
                if file_type and self.db_handler:
                    patterns = self.db_handler.get_patterns().get(file_type, [])
                
                for item in directory.rglob('*'):
                    if item.is_file():
                        # Check size constraints
                        size = item.stat().st_size
                        if min_size and size < min_size:
                            continue
                        if max_size and size > max_size:
                            continue
                        
                        # Check file type patterns
                        if patterns:
                            matches = False
                            for pattern in patterns:
                                if item.match(pattern):
                                    matches = True
                                    break
                            if not matches:
                                continue
                        
                        files.append({
                            'path': str(item),
                            'size': size,
                            'modified': item.stat().st_mtime,
                            'type': self._get_file_type(item)
                        })
        except Exception as e:
            self.logger.error(f"Error scanning {directory}: {e}")
        return files
    
    def scan_multiple_directories(self, directories: List[Path]) -> List[Dict]:
        """Scan multiple directories"""
        all_files = []
        for directory in directories:
            all_files.extend(self.scan_directory(directory))
        return all_files
    
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
            ]
        }