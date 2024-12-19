# Mac Cleaner

A professional-grade system cleaning tool for macOS with a focus on privacy, safety, and performance optimization. All operations are performed locally on your machine with zero data collection.

## Project Status
🚧 **Under Development** - Following strict TDD, clean architecture principles, and privacy-first design

## Key Principles
- 🔒 **Privacy First**: All operations are local, no data collection
- 🛡️ **Zero Knowledge**: We can't access your data, even if we wanted to
- 🔐 **Data Protection**: Secure operations with privacy-safe logging
- ⚡ **Performance**: Efficient system optimization
- 🎯 **User Control**: Full transparency and control over all operations

## Features
### Implemented ✅
- Privacy-Safe Disk Analysis
  - Local-only disk usage information
  - Privacy-respecting path analysis
  - Secure data handling
- Secure Memory Monitoring
  - Private system memory analysis
  - Local process-level tracking
  - Privacy-aware resource monitoring
  - Secure error handling

### Coming Soon 📅
- System health checks
- Safe cleaning operations
- Full undo capability
- Modern CLI interface
- Comprehensive safety checks

## Documentation
Our documentation is organized into three main areas:

### 1. Architecture (`docs/architecture/`)
- [System Overview](docs/architecture/README.md)
- [Architecture Decisions](docs/architecture/decisions/)
- [Component Documentation](docs/architecture/components/)
- [System Diagrams](docs/architecture/diagrams/)

### 2. Development (`docs/development/`)
- [Contributing Guide](docs/development/CONTRIBUTING.md)
- [Development Framework](DEVELOPMENT_FRAMEWORK.md)
- [Style Guide](docs/development/STYLE.md)

### 3. Project (`docs/project/`)
- [Project Charter](docs/project/PROJECT_CHARTER.md)
- [Progress Tracking](PROGRESS.md)
- [Changelog](docs/project/CHANGELOG.md)

## Getting Started
```bash
# Clone the repository
git clone [repository-url]
cd mac-cleaner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Development Process
1. Check [PROGRESS.md](PROGRESS.md) for current sprint and available tasks
2. Follow guidelines in [DEVELOPMENT_FRAMEWORK.md](DEVELOPMENT_FRAMEWORK.md)
3. Read [Contributing Guide](docs/development/CONTRIBUTING.md) for workflow
4. Review [Architecture](docs/architecture/README.md) for system design

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This tool is for educational purposes. Always backup your system before using cleaning tools.
