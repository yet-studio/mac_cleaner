# Mac Cleaner

A powerful system cleaning tool for macOS that helps you manage and clean system directories efficiently.

## Features

- Clean system directories and temporary files
- Calculate potential space savings before cleaning
- Smart permission handling with sudo support
- Multiple cleaning categories (cache, logs, etc.)
- Size estimation and preview before cleaning
- Fast and efficient cleaning operations
- Undo/backup capability for safe cleaning

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mac-cleaner.git
cd mac-cleaner
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python main.py
```

### With Root Privileges (for system directories)
```bash
sudo python main.py
```

The cleaner will:
1. Scan your system for cleanable files
2. Show potential space savings
3. Ask for confirmation before cleaning
4. Clean files with appropriate permissions
5. Show a summary of cleaned and failed items

## Development

### Running Tests
```bash
pytest -v
```

### Code Coverage
```bash
pytest --cov=src tests/
```

Current code coverage: 89%

### Project Structure
```
mac-cleaner/
├── src/
│   ├── core/          # Core cleaning functionality
│   ├── database/      # Database operations
│   ├── history/       # Cleaning history
│   ├── ui/           # User interface
│   ├── undo/         # Backup/restore
│   └── utils/        # Utility functions
├── tests/            # Test suite
└── main.py          # Main entry point
```

## Recent Updates (2024-12-19)

- Enhanced permission handling with better sudo detection
- Improved error messages for inaccessible directories
- Added accurate size calculation for cleaned files
- Implemented TDD approach for feature development
- Enhanced test coverage for permission-related scenarios

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests first (TDD)
4. Implement your changes
5. Run tests and ensure coverage
6. Submit a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.