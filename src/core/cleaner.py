from pathlib import Path
from typing import List, Dict, Optional
import logging
import shutil
from datetime import datetime

class FileCleaner:
    """Core cleaner functionality"""
    
    def __init__(self, backup_manager=None, history_manager=None):
        self.backup_manager = backup_manager
        self.history_manager = history_manager
        self.logger = logging.getLogger(__name__)
    
    def clean_files(self, files: List[Dict], backup: bool = True) -> Dict:
        """Clean files with optional backup"""
        results = {
            'cleaned': [],
            'failed': [],
            'total_size': 0,
            'backup_id': None
        }
        
        # Create backup if requested
        if backup and self.backup_manager and files:
            try:
                backup_id = self.backup_manager.create_backup(
                    [file['path'] for file in files]
                )
                results['backup_id'] = backup_id
            except Exception as e:
                self.logger.error(f"Backup failed: {e}")
                return results
        
        # Clean files
        for file in files:
            try:
                path = Path(file['path'])
                if path.exists():
                    path.unlink()
                    results['cleaned'].append(file)
                    results['total_size'] += file['size']
            except Exception as e:
                self.logger.error(f"Failed to clean {file['path']}: {e}")
                results['failed'].append({
                    'file': file,
                    'error': str(e)
                })
        
        # Log operation
        if self.history_manager:
            self._log_operation(results)
        
        return results
    
    def clean_by_type(self, scan_results: Dict[str, List[Dict]], 
                      types: Optional[List[str]] = None) -> Dict:
        """Clean files by type"""
        if types is None:
            types = list(scan_results.keys())
        
        files_to_clean = []
        for file_type in types:
            if file_type in scan_results:
                files_to_clean.extend(scan_results[file_type])
        
        return self.clean_files(files_to_clean)
    
    def _log_operation(self, results: Dict):
        """Log cleaning operation"""
        operation = {
            'timestamp': datetime.now().isoformat(),
            'cleaned_count': len(results['cleaned']),
            'failed_count': len(results['failed']),
            'total_size': results['total_size'],
            'backup_id': results['backup_id']
        }
        
        try:
            self.history_manager.add_entry(operation)
        except Exception as e:
            self.logger.error(f"Failed to log operation: {e}")
    
    def estimate_space_saving(self, files: List[Dict]) -> int:
        """Estimate space that would be freed"""
        return sum(file['size'] for file in files)
    
    def verify_cleaning(self, results: Dict) -> bool:
        """Verify cleaning operation"""
        for file in results['cleaned']:
            if Path(file['path']).exists():
                return False
        return True