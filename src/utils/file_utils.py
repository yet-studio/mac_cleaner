"""File utility functions"""
from typing import List, Dict, Any, Union

def format_size(size_bytes: float) -> str:
    """Format size in bytes to human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string with appropriate unit
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def collect_files_to_clean(paths_by_category: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Collect files that need to be cleaned from all categories
    
    Args:
        paths_by_category: Dictionary of paths organized by category
        
    Returns:
        List of files to clean with their sizes
    """
    files_to_clean = []
    for paths in paths_by_category.values():
        for path_info in paths:
            if path_info['size'] > 0:
                files_to_clean.append(path_info)
    return files_to_clean

def calculate_total_size(paths_by_category: Dict[str, List[Dict[str, Any]]]) -> int:
    """Calculate total size of all files in all categories
    
    Args:
        paths_by_category: Dictionary of paths organized by category
        
    Returns:
        Total size in bytes
    """
    return sum(
        path_info['size']
        for paths in paths_by_category.values()
        for path_info in paths
    )