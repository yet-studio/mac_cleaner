"""System cleaner UI module"""
from typing import Dict, List, Any, Optional
from src.core.cleaner import get_system_paths
from src.utils.file_utils import format_size

class SystemCleanerUI:
    """User interface for system cleaning operations"""
    
    @staticmethod
    def display_category_info(category: str, paths: List[Dict]) -> None:
        """Display information about a category of paths
        
        Args:
            category: Category name
            paths: List of paths with sizes
        """
        total_size = sum(path.get('size', 0) for path in paths)
        if total_size == 0:
            return
            
        print(f"\n{category} ({format_size(total_size)}):")
        for path in paths:
            if path.get('size', 0) > 0:
                print(f"  - {path['path']} ({format_size(path['size'])})")
    
    @staticmethod
    def display_cleaning_results(results: Dict[str, List]) -> None:
        """Display results of cleaning operation
        
        Args:
            results: Dictionary containing cleaned and failed items
        """
        # Display progress for each item
        cleaned = results.get('cleaned', [])
        failed = results.get('failed', [])
        
        if cleaned:
            print(f"\nSuccessfully cleaned {len(cleaned)} items")
        
        if failed:
            print(f"\nFailed to clean {len(failed)} items:")
            permission_errors = [f for f in failed if "Operation not permitted" in f['error']]
            other_errors = [f for f in failed if "Operation not permitted" not in f['error']]
            
            if permission_errors:
                print("\nPermission denied for the following directories:")
                for item in permission_errors:
                    print(f"  - {item['path']}")
                print("\nTo clean these directories, please run with sudo:")
                print("    sudo python main.py")
            
            if other_errors:
                print("\nOther errors:")
                for item in other_errors:
                    print(f"  - {item['path']}: {item['error']}")
    
    @staticmethod
    def confirm_cleaning() -> bool:
        """Get user confirmation for cleaning
        
        Returns:
            bool: True if user confirms, False otherwise
        """
        response = input("\nDo you want to clean these directories? [y/N] ")
        return response.lower() == 'y'
    
    @staticmethod
    def display_root_warning() -> None:
        """Display warning about root privileges"""
        print("\nWarning: Some system directories may require root privileges.")
        print("To clean all directories, run with 'sudo python main.py'")
        print("Without sudo, only user-accessible directories will be cleaned.\n")
    
    @staticmethod
    def display_cleaning_summary(cleaned_size: int) -> None:
        """Display summary of cleaned space
        
        Args:
            cleaned_size: Total size cleaned in bytes
        """
        if cleaned_size > 0:
            print(f"\nTotal space freed: {format_size(cleaned_size)}")
