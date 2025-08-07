# Claude Code Setup

This repository contains Claude Code configuration files including agents and commands.

This is a `work in progress`. More features and commands will be added over time.

## Installation

Follow these steps to set up Claude Code:

### 1. Clone the repository
```bash
git clone https://github.com/neurifai/claude-code.git
cd claude-code
```

### 2. Make the setup script executable
```bash
chmod +x setup.sh
```

### 3. Run the setup script
```bash
./setup.sh
```

This will:
- Check for Python 3.11 and provide installation instructions if not found
- Create a Python virtual environment if Python 3.11 is available
- Create the `~/.claude` directory if it doesn't exist
- Copy the `agents` and `commands` folders to `~/.claude`

After setup, activate the virtual environment (if created):
```bash
source .venv/bin/activate
```

## Requirements
- Git
- Bash shell
- Python 3.11 (recommended for Python-based commands)
  - macOS: `brew install python@3.11`
  - Ubuntu/Debian: `sudo apt-get install python3.11`
  - Other: Visit [python.org](https://www.python.org/downloads/)