from pathlib import Path

def create_project_structure():
    """Create the basic project structure"""
    # Get current working directory
    base_dir = Path.cwd()
    print(f"Creating project structure in: {base_dir}")
    
    # Define project structure
    structure = {
        'src': {
            'core': ['__init__.py', 'cleaner.py', 'scanner.py'],
            'database': ['__init__.py', 'db_handler.py'],
            'ui': ['__init__.py', 'cli.py', 'messages.py'],
            'utils': ['__init__.py', 'file_utils.py'],
            'history': ['__init__.py', 'history_manager.py'],
            'undo': ['__init__.py', 'backup_manager.py', 'restore_manager.py'],
            '__init__.py': None
        },
        'tests': {
            '__init__.py': None,
            'test_cleaner.py': None,
            'test_scanner.py': None
        },
        'logs': {'.gitkeep': None},
        'backups': {'.gitkeep': None},
        'config': {'settings.json': None},
        'pyproject.toml': None,
        'README.md': None
    }
    
    def create_structure(parent_path, structure_dict):
        for name, content in structure_dict.items():
            path = parent_path / name
            
            if isinstance(content, dict):
                # Create directory
                path.mkdir(exist_ok=True)
                print(f"Created directory: {path}")
                create_structure(path, content)
            elif isinstance(content, list):
                # Create directory for files
                path.mkdir(exist_ok=True)
                print(f"Created directory: {path}")
                # Create files in directory
                for file_name in content:
                    file_path = path / file_name
                    file_path.touch()
                    print(f"Created file: {file_path}")
            else:
                # Create single file
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
                print(f"Created file: {path}")
    
    create_structure(base_dir, structure)
    
    # Create pyproject.toml content
    pyproject_content = '''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mac_cleaner"
version = "1.0.0"
description = "A Mac system cleaner with undo capability"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "pathlib",
    "typing",
]

[project.optional-dependencies]
test = ["pytest"]
'''
    
    # Write pyproject.toml
    with open(base_dir / 'pyproject.toml', 'w') as f:
        f.write(pyproject_content)
    
    print("\nProject structure created successfully!")
    print("You can now start implementing the core functionality.")

if __name__ == "__main__":
    create_project_structure()
