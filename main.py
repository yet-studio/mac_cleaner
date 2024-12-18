#!/usr/bin/env python3
"""Mac Cleaner - System cleaning tool for macOS"""

import sys
import os
from typing import NoReturn

from src.core.cleaner import FileCleaner, get_system_paths
from src.ui.system_cleaner import SystemCleanerUI
from src.utils.file_utils import format_size, collect_files_to_clean, calculate_total_size

def _create_path_size_map(paths_by_category):
    """Create a mapping of file paths to their sizes.
    
    Args:
        paths_by_category (dict): Dictionary of paths organized by category
        
    Returns:
        dict: Mapping of file paths to their sizes
    """
    return {path['path']: path.get('size', 0) 
            for paths in paths_by_category.values() 
            for path in paths}

def clean_system_paths() -> None:
    """Clean system directories"""
    ui = SystemCleanerUI()
    
    # Check if running with sudo
    use_sudo = os.geteuid() == 0
    
    # Get system paths with size information
    paths_by_category = get_system_paths(with_size=True)
    
    # Filter out paths with no size or no access
    accessible_paths = {}
    total_size = 0
    for category, paths in paths_by_category.items():
        accessible = []
        for path in paths:
            if path.get('size', 0) > 0 and (use_sudo or os.access(path['path'], os.W_OK)):
                accessible.append(path)
                total_size += path.get('size', 0)
        if accessible:
            accessible_paths[category] = accessible
    
    if not accessible_paths:
        print("\nNo cleanable directories found!")
        if not use_sudo:
            print("Try running with sudo to access system directories.")
        return
    
    # Display information about files to clean
    print("\nAnalyzing system directories...")
    
    for category, paths in accessible_paths.items():
        ui.display_category_info(category, paths)
    
    print(f"\nTotal potential space savings: {format_size(total_size)}")
    
    # Get user confirmation
    if not ui.confirm_cleaning():
        print("Operation cancelled.")
        return
    
    # Clean the files
    print("\nCleaning files...")
    cleaner = FileCleaner(use_sudo=use_sudo)
    
    # Create a mapping of paths to their sizes for later use
    path_sizes = _create_path_size_map(accessible_paths)
    
    # Clean the files
    results = cleaner.clean_files([{'path': path['path']} 
                                 for paths in accessible_paths.values() 
                                 for path in paths])
    
    # Calculate cleaned size using the path_sizes mapping
    cleaned_size = sum(path_sizes.get(path, 0) for path in results.get('cleaned', []))
    
    # Display results
    ui.display_cleaning_results(results)
    ui.display_cleaning_summary(cleaned_size)

def main() -> None:
    """Main entry point"""
    print("Welcome to the Mac Cleaner App!")
    
    # Check if running with sudo and display appropriate message
    use_sudo = os.geteuid() == 0
    if not use_sudo:
        SystemCleanerUI.display_root_warning()
    
    try:
        clean_system_paths()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        if not use_sudo and "Operation not permitted" in str(e):
            print("\nTry running with sudo to clean system directories:")
            print("    sudo python main.py")

if __name__ == '__main__':
    main()
