Create a new task file with structured template

# Task Command

Creates a structured task file in `.claude/tasks/` with the provided task name and description. 
This command ONLY creates the file structure - it does not generate plans or execute code.

## Usage
/task "User Authentication" Implement secure user authentication system with JWT tokens, password hashing, and session management
/task "Payment Bug Fix" Fix the bug in payment processing where transactions fail for amounts over $1000
/task "Reports API" Add new API endpoint for generating and retrieving user activity reports

## Backward Compatibility
/task implement user authentication (still works - uses entire text as both name and description)

## What it does
1. Parses task name (in quotes) and detailed description
2. Assesses task complexity automatically (easy/medium/hard)
3. Creates a timestamped task file using the task name
4. Populates it with structured template including the detailed description
5. Confirms task file creation and provides next steps

## Complexity Assessment
The command automatically assesses task complexity based on keywords and patterns:

- **Easy**: Simple changes, bug fixes, styling, single file modifications
- **Medium**: Components, services, refactoring, multiple steps
- **Hard**: Backend systems, APIs, databases, architecture, security, integrations

## New Workflow
1. **Create task**: `/task "Task Name" detailed description`
2. **Edit context** (optional): Manually edit the task file to add more context
3. **Plan implementation**: `/task-plan task-name-slug` to generate detailed execution plan
4. **Execute**: `/task-exec task-name-slug` to execute the planned implementation

## Why the Change?
This separation allows you to:
- Get the task file created quickly
- Add additional context manually before planning begins
- Have more control over the planning process
- Maintain a clear workflow: create → edit → plan → execute
