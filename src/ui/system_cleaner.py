"""System cleaner UI module"""
from typing import Dict, List, Any, Optional
from src.core.cleaner import get_system_paths
from src.utils.file_utils import format_size

class SystemCleanerUI:
    """User interface for system cleaning operations"""
    
    @staticmethod
    def display_category_info(category: str, paths: List[Dict[str, Any]]) -> None:
        """Display information about a category of paths"""
        category_size = sum(path_info['size'] for path_info in paths)
        if category_size > 0:
            print(f"\n{category.upper()} ({format_size(category_size)}):")
            for path_info in paths:
                if path_info['size'] > 0:
                    print(f"  - {path_info['path']} ({format_size(path_info['size'])})")

    @staticmethod
    def display_cleaning_results(results: Dict[str, List[Any]]) -> None:
        """Display the results of cleaning operation"""
        if results['cleaned']:
            print(f"\nSuccessfully cleaned {len(results['cleaned'])} items")
        if results['failed']:
            print(f"\nFailed to clean {len(results['failed'])} items:")
            for failure in results['failed']:
                print(f"  - {failure['path']}: {failure['error']}")

    @staticmethod
    def confirm_cleaning() -> bool:
        """Ask user for confirmation before cleaning"""
        response = input("\nDo you want to clean these directories? [y/N] ").lower()
        return response == 'y'

    @staticmethod
    def display_root_warning() -> None:
        """Display warning about root privileges"""
        print("\nWarning: Some system directories may require root privileges.")
        print("Consider running with sudo for full cleaning capabilities.")
