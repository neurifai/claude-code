# Claude Code Setup

This repository contains Claude Code configuration files including agents and commands.

This is a `work in progress`. More features and commands will be added over time.

# What You Get

## Custom Commands

### `/task` - Task Creation
Creates structured task files with automatic complexity assessment (easy/medium/hard).
- **Usage**: `/task "Task Name" detailed description`
- **Example**: `/task "User Auth" Implement JWT-based authentication with refresh tokens`
- Creates timestamped task files in `.claude/tasks/` for tracking and organization

### `/task-plan` - Task Planning
Generates detailed execution plans for existing tasks without implementing code.
- **Usage**: `/task-plan task-name-slug`
- Analyzes codebase architecture and patterns
- Creates comprehensive implementation roadmap with specific todos
- Follows CLAUDE.md patterns or detects existing conventions
- Uses thinking mode for complex architectural decisions

### `/task-exec` - Task Execution
Executes previously planned tasks with real-time progress tracking.
- **Usage**: `/task-exec task-name-slug`
- Follows the execution plan step-by-step
- Updates task file with progress logs and completed todos
- Handles errors gracefully with detailed documentation
- Maintains timestamped progress tracking

### `/help` - Command Documentation
Displays help for available custom commands.
- **Usage**: `/help` (list all) or `/help <command>` (specific help)
- Provides detailed documentation for each command
- Shows usage examples and workflow guidance

## Workflow Example
```bash
# 1. Create a new task
/task "Payment Integration" Add Stripe payment processing with webhook handling

# 2. Review and optionally edit the task file manually

# 3. Generate detailed plan
/task-plan payment-integration

# 4. Execute the implementation
/task-exec payment-integration
```

## Custom Agents

### `security-architect-reviewer`
A Principal Security Engineer agent specialized in security analysis and vulnerability assessment.

**Capabilities**:
- **Code Security Review**: Identifies OWASP Top 10 vulnerabilities, injection flaws, XSS, CSRF, authentication weaknesses
- **Architecture Assessment**: Evaluates defense-in-depth, zero trust principles, encryption strategies, secrets management
- **Actionable Recommendations**: Provides severity classifications, specific fixes with code examples, and preventive measures

**When to use**:
- After implementing authentication/authorization systems
- When handling sensitive data or PII
- For microservices security architecture review
- To audit existing code for vulnerabilities
- When implementing encryption or secure communication

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

### 4. **⚠️ IMPORTANT: Manually merge the settings.json content**

**You MUST manually merge the settings from this repository into your ~/.claude/settings.json file:**

**DO NOT simply copy/overwrite the file - you may lose existing custom settings!**

**Steps to merge:**
1. Open `.claude/settings.json` from this repository
2. Open your global settings file `~/.claude/settings.json` (create it if it doesn't exist)
3. Copy the `commands` and `agents` sections from the repo's settings.json
4. Add them to your global settings.json, preserving any existing configurations

**Why manual merge?** This ensures you don't accidentally overwrite any custom commands, agents, or other settings you may already have configured.

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