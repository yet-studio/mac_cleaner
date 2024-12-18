#!/usr/bin/env python3
"""Mac Cleaner - System cleaning tool for macOS"""

import sys
import os
from typing import NoReturn

from src.core.cleaner import FileCleaner, get_system_paths
from src.ui.system_cleaner import SystemCleanerUI
from src.utils.file_utils import format_size, collect_files_to_clean, calculate_total_size

def clean_system_paths() -> None:
    """Clean system directories"""
    ui = SystemCleanerUI()
    
    # Get system paths with size information
    paths_by_category = get_system_paths(with_size=True)
    
    # Collect files to clean
    files_to_clean = collect_files_to_clean(paths_by_category)
    if not files_to_clean:
        print("\nNo files to clean!")
        return
    
    # Display information about files to clean
    print("\nAnalyzing system directories...")
    total_size = calculate_total_size(paths_by_category)
    
    for category, paths in paths_by_category.items():
        ui.display_category_info(category, paths)
    
    print(f"\nTotal potential space savings: {format_size(total_size)}")
    
    # Get user confirmation
    if not ui.confirm_cleaning():
        print("Operation cancelled.")
        return
    
    # Clean the files
    print("\nCleaning files...")
    cleaner = FileCleaner()
    results = cleaner.clean_files(files_to_clean)
    
    # Display results
    ui.display_cleaning_results(results)

def main() -> NoReturn:
    """Main entry point"""
    print("Welcome to the Mac Cleaner App!")
    
    # Check if running with sudo
    if os.geteuid() != 0:
        SystemCleanerUI.display_root_warning()
    
    try:
        clean_system_paths()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
    
    sys.exit(0)

if __name__ == '__main__':
    main()
