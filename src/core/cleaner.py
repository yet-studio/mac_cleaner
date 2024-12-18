from pathlib import Path
from typing import List, Dict, Optional, Union, Any
import logging
import os

class FileCleaner:
    """Cleaner for removing files"""
    
    def __init__(self, backup_manager=None, history_manager=None):
        self.backup_manager = backup_manager
        self.history_manager = history_manager
        self.logger = logging.getLogger(__name__)
    
    def clean_files(self, files: List[Dict], backup: bool = False) -> Dict:
        """Clean files with optional backup"""
        if not isinstance(files, list):
            raise ValueError("Files must be a list")
        
        results = {'cleaned': [], 'failed': []}
        
        for file_info in files:
            try:
                file_path = Path(file_info['path'])
                if not file_path.exists():
                    results['failed'].append({**file_info, 'error': 'File does not exist'})
                    continue
                    
                file_path.unlink()
                results['cleaned'].append(file_info)
                
            except Exception as e:
                results['failed'].append({**file_info, 'error': str(e)})
                
        return results
    
    def clean_by_pattern(self, directory: Union[str, Path], patterns: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Clean files matching the given patterns in the directory."""
        results = {'cleaned': [], 'failed': []}
        try:
            directory = Path(directory)
            if not directory.exists():
                results['failed'].append({'path': str(directory), 'error': 'Directory does not exist'})
                return results

            for root, _, files in os.walk(str(directory)):
                for file_name in files:
                    if any(file_name.endswith(pattern.lstrip('*')) for pattern in patterns):
                        file_path = Path(root) / file_name
                        try:
                            file_size = file_path.stat().st_size
                            file_path.unlink()
                            results['cleaned'].append({
                                'path': str(file_path),
                                'size': file_size
                            })
                        except Exception as e:
                            results['failed'].append({
                                'path': str(file_path),
                                'error': str(e)
                            })

        except Exception as e:
            self.logger.error(f"Error in clean_by_pattern: {e}")
            results['failed'].append({
                'path': str(directory),
                'error': str(e)
            })

        return results

    def estimate_space_saving(self, files: List[Dict]) -> int:
        """Estimate space that would be freed by cleaning files"""
        return sum(file.get('size', 0) for file in files)