# Mac Cleaner

A powerful and safe system cleaning tool for macOS with backup and restore capabilities.

## Features

- **Smart Cleaning**: Identifies and removes temporary files and logs
- **System Paths**: Pre-configured paths for common system cleanup locations:
  - Cache files (`~/Library/Caches`, `/Library/Caches`)
  - Container files (`~/Library/Containers`)
  - Application state (`~/Library/Saved Application State`)
  - Temporary files (`/private/tmp`)
  - Log files (`~/Library/Logs`, `/var/log`, etc.)
- **File Preview**: Preview file contents before deletion
- **Backup System**: Creates backups before any deletion
- **Undo Support**: Restore deleted files if needed
- **Cleaning History**: Tracks all cleaning operations
- **Safe Operations**: Confirms actions before deletion
- **Detailed Logging**: Maintains comprehensive logs of all operations

## Project Structure

```
mac_cleaner/
├── src/                    # Source code
│   ├── core/              # Core functionality
│   │   ├── cleaner.py     # Cleaning operations
│   │   └── scanner.py     # File scanning
│   ├── database/          # Database operations
│   │   └── db_handler.py  # Database management
│   ├── ui/                # User interface
│   │   ├── cli.py        # Command-line interface
│   │   └── messages.py   # User messages
│   ├── utils/             # Utility functions
│   │   └── file_utils.py # File operations
│   ├── history/           # Operation history
│   │   └── history_manager.py
│   └── undo/              # Backup/restore
│       ├── backup_manager.py
│       └── restore_manager.py
├── tests/                 # Test suite
├── logs/                  # Application logs
├── backups/              # File backups
└── config/               # Configuration files
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd mac-cleaner
```

2. Install dependencies:
```bash
pip install -e .
```

## Usage

1. **Basic Cleaning**:
```bash
python main.py
```

2. **Preview Files Before Cleaning**:
```python
from src.core.cleaner import FileCleaner

cleaner = FileCleaner()
preview = cleaner.preview_files([{'path': '/path/to/file'}])
```

3. **Clean System Paths**:
```python
from src.core.cleaner import get_system_paths

# Get all system paths
paths = get_system_paths()

# Get paths by category (cache, logs, etc.)
cache_paths = get_system_paths(category='cache')

# Get paths with size information
paths_with_size = get_system_paths(with_size=True)
```

4. **View Cleaning History**:
- Select option 2 from the main menu

5. **Restore Files**:
- Select option 3 from the main menu
- Choose the backup to restore from

## Safety Features

1. **Pre-deletion Backup**
   - Automatic backup creation before any deletion
   - Backups stored in `backups/` directory
   - Complete manifest of backed-up files

2. **Confirmation System**
   - User confirmation required before deletion
   - Preview of files to be deleted
   - Size impact information

3. **Restore Capability**
   - Multiple backup points
   - Full or selective restoration
   - Backup browsing and selection

## Configuration

### System Paths

System cleanup paths are configured in `config/system_paths.json`. The paths are organized by categories:

```json
{
    "cleanup_paths": {
        "cache": [
            "/Users/[user]/Library/Caches",
            "/Library/Caches"
        ],
        "logs": [
            "/Users/[user]/Library/Logs",
            "/var/log"
        ],
        ...
    }
}
```

You can customize these paths by editing the configuration file.

## Development

### Setting up development environment

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

2. Install development dependencies:
```bash
pip install -e ".[test]"
```

### Running Tests

```bash
pytest tests/
```

### Project Components

1. **Core (src/core/)**
   - `scanner.py`: File system scanning
   - `cleaner.py`: Cleaning operations

2. **Database (src/database/)**
   - Manages cleaning locations
   - Tracks file patterns

3. **UI (src/ui/)**
   - Command-line interface
   - User interaction handling

4. **History (src/history/)**
   - Tracks cleaning operations
   - Maintains operation logs

5. **Undo System (src/undo/)**
   - Backup management
   - File restoration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:
1. Check the documentation
2. Look through existing issues
3. Create a new issue if needed

## Roadmap

- [ ] GUI Implementation
- [ ] Advanced scanning patterns
- [ ] Custom cleaning rules
- [ ] Schedule cleaning operations
- [ ] System integration
- [ ] Multiple backup locations