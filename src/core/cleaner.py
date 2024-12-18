from pathlib import Path
from typing import List, Dict, Optional, Union, Any
import logging
import os
import json

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

    def _get_file_preview(self, file_path: Path) -> Dict[str, Any]:
        """Get preview information for a single file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing file preview information
        """
        result = {'path': str(file_path)}
        
        try:
            if not file_path.exists():
                result['error'] = 'File does not exist'
                return result
            
            # Get file size
            result['size'] = file_path.stat().st_size
            
            # Read first 100 characters of the file
            try:
                with open(file_path, 'r') as f:
                    result['content_preview'] = f.read(100)
            except UnicodeDecodeError:
                result['content_preview'] = '<binary file>'
                
        except PermissionError:
            result['error'] = 'Permission denied'
        except Exception as e:
            result['error'] = str(e)
            
        return result

    def preview_files(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Preview files before cleaning them.
        
        Args:
            files: List of dictionaries containing file paths
            
        Returns:
            List of dictionaries containing file information and previews
        """
        if not isinstance(files, list):
            raise ValueError("Files must be provided as a list")
            
        return [self._get_file_preview(Path(file_info['path'])) 
                for file_info in files]

    def estimate_space_saving(self, files: List[Dict]) -> int:
        """Estimate space that would be freed by cleaning files"""
        return sum(file.get('size', 0) for file in files)

def get_system_paths(category: Optional[str] = None, check_exists: bool = False, with_size: bool = False) -> Union[Dict[str, List[Union[str, Dict[str, Any]]]], List[Union[str, Dict[str, Any]]]]:
    """Get system paths for cleaning from configuration.
    
    Args:
        category: Optional category to filter paths
        check_exists: Only return paths that exist
        with_size: Include size information for each path
        
    Returns:
        Dictionary of paths by category or list of paths if category is specified
    """
    config_path = Path(__file__).parent.parent.parent / 'config' / 'system_paths.json'
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    paths = config['cleanup_paths']
    
    if category:
        if category not in paths:
            raise ValueError(f"Invalid category: {category}")
        paths = paths[category]
    
    def process_path(path: str) -> Union[str, Dict[str, Any]]:
        path_obj = Path(path)
        if check_exists and not path_obj.exists():
            return None
        
        if with_size:
            try:
                size = sum(f.stat().st_size for f in path_obj.rglob('*') if f.is_file())
            except (PermissionError, FileNotFoundError):
                size = 0
            return {'path': path, 'size': size}
        return path
    
    if category:
        processed = [process_path(p) for p in paths]
        return [p for p in processed if p is not None]
    
    result = {}
    for cat, path_list in paths.items():
        processed = [process_path(p) for p in path_list]
        result[cat] = [p for p in processed if p is not None]
    
    return result