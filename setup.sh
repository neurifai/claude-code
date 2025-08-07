#!/bin/bash

set -e

CLAUDE_HOME="$HOME/.claude"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Claude Code Setup Script"
echo "========================"
echo

# Check for Python 3.11
echo "Checking for Python 3.11..."
PYTHON_CMD=""

# Check for python3.11 command
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo "Found Python 3.11 at: $(which python3.11)"
    echo "Version: $(python3.11 --version)"
# Check if python3 is version 3.11
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    if [[ "$PYTHON_VERSION" == "3.11" ]]; then
        PYTHON_CMD="python3"
        echo "Found Python 3.11 at: $(which python3)"
        echo "Version: $(python3 --version)"
    else
        echo "Warning: Python 3 found but version is $PYTHON_VERSION (3.11 recommended)"
        echo "Continuing with setup, but consider installing Python 3.11 for best compatibility."
    fi
# Check if python is version 3.11
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    if [[ "$PYTHON_VERSION" == "3.11" ]]; then
        PYTHON_CMD="python"
        echo "Found Python 3.11 at: $(which python)"
        echo "Version: $(python --version)"
    else
        echo "Warning: Python found but version is $PYTHON_VERSION (3.11 recommended)"
        echo "Continuing with setup, but consider installing Python 3.11 for best compatibility."
    fi
else
    echo "Warning: Python not found. Python 3.11 is recommended for running Python-based commands."
    echo "You can install it using:"
    echo "  - macOS: brew install python@3.11"
    echo "  - Ubuntu/Debian: sudo apt-get install python3.11"
    echo "  - Other: Visit https://www.python.org/downloads/"
    echo
    echo "Continuing with setup..."
fi

# Setup virtual environment if Python 3.11 is available
if [ ! -z "$PYTHON_CMD" ]; then
    VENV_DIR="$SCRIPT_DIR/.venv"
    if [ ! -d "$VENV_DIR" ]; then
        echo
        echo "Creating Python virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        echo "Virtual environment created at: $VENV_DIR"
        
        # Activate and upgrade pip
        source "$VENV_DIR/bin/activate"
        pip install --upgrade pip > /dev/null 2>&1
        echo "Virtual environment is ready. Activate it with: source .venv/bin/activate"
    else
        echo "Virtual environment already exists at: $VENV_DIR"
    fi
fi

echo

if [ ! -d "$CLAUDE_HOME" ]; then
    echo "Creating ~/.claude directory..."
    mkdir -p "$CLAUDE_HOME"
    echo "~/.claude directory created."
else
    echo "~/.claude directory already exists."
fi

if [ -d "$SCRIPT_DIR/.claude/agents" ]; then
    echo "Copying agents folder to ~/.claude..."
    cp -r "$SCRIPT_DIR/.claude/agents" "$CLAUDE_HOME/"
    echo "Agents folder copied successfully."
else
    echo "Warning: agents folder not found in $SCRIPT_DIR/.claude/"
fi

if [ -d "$SCRIPT_DIR/.claude/commands" ]; then
    echo "Copying commands folder to ~/.claude..."
    cp -r "$SCRIPT_DIR/.claude/commands" "$CLAUDE_HOME/"
    echo "Commands folder copied successfully."
else
    echo "Warning: commands folder not found in $SCRIPT_DIR/.claude/"
fi

echo
echo -e "\033[32m========================================="
echo -e "IMPORTANT: Manual Configuration Required"
echo -e "=========================================\033[0m"
echo
echo -e "\033[32mYou must manually merge the settings from this repository into your ~/.claude/settings.json file.\033[0m"
echo
echo -e "\033[32mDO NOT simply copy/overwrite the file as you may have existing custom settings!\033[0m"
echo
echo -e "\033[32mSteps:\033[0m"
echo -e "\033[32m1. Open the settings file from this repo: $SCRIPT_DIR/.claude/settings.json\033[0m"
echo -e "\033[32m2. Open your global settings file: ~/.claude/settings.json (create it if it doesn't exist)\033[0m"
echo -e "\033[32m3. Manually copy the 'hooks' sections into your global settings\033[0m"
echo -e "\033[32m4. Make sure to preserve any existing settings you already have\033[0m"
echo
echo -e "\033[32mThis manual merge ensures you don't lose any existing custom commands or configurations.\033[0m"
echo
echo -e "\033[32m=========================================\033[0m"
echo
echo "Setup completed successfully!"
echo "Claude configuration files have been installed to: $CLAUDE_HOME"