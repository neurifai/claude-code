#!/usr/bin/env python3
import json
import sys
import os
import glob
import re
from datetime import datetime


def check_task_status(task_file):
    """Check if task is already completed or blocked"""
    try:
        with open(task_file, 'r') as f:
            content = f.read()

        if "## Final Status" in content:
            status_section = content.split("## Final Status")[1].split("##")[0] if "##" in \
                                                                                   content.split("## Final Status")[
                                                                                       1] else \
            content.split("## Final Status")[1]
            if "COMPLETED" in status_section.upper():
                return "completed"
            elif "FAILED" in status_section.upper():
                return "failed"
            elif "BLOCKED" in status_section.upper():
                return "blocked"

        # Check if all todos are done
        if "- [ ]" not in content and "- [x]" in content:
            return "likely_completed"

        return "ready"
    except:
        return "unknown"


def get_execution_strategy(task_file):
    """Determine execution approach based on task complexity"""
    try:
        with open(task_file, 'r') as f:
            content = f.read()

        if "**Assessed Complexity:** EASY" in content:
            return {
                "strategy": "sequential",
                "use_agents": False,
                "validation_level": "basic",
                "commit_frequency": "end"
            }
        elif "**Assessed Complexity:** HARD" in content:
            return {
                "strategy": "phased",
                "use_agents": True,
                "validation_level": "comprehensive",
                "commit_frequency": "per-phase"
            }
        else:  # medium
            return {
                "strategy": "sequential",
                "use_agents": False,
                "validation_level": "standard",
                "commit_frequency": "milestone"
            }
    except:
        return {
            "strategy": "sequential",
            "use_agents": False,
            "validation_level": "standard",
            "commit_frequency": "end"
        }


def validate_task_ready(task_file):
    """Validate that task file is properly planned and ready for execution"""
    validation_errors = []

    try:
        with open(task_file, 'r') as f:
            content = f.read()

        # Check for execution plan
        if "## Implementation Plan" not in content and "## Execution Plan" not in content:
            validation_errors.append("Missing execution plan section")

        # Check for file modifications table or structured plan
        if "## File Modifications" not in content and "| File Path |" not in content and "### File Modifications Table" not in content:
            validation_errors.append("Missing file modifications table")

        # Check for uncompleted todos
        if not re.search(r'- \[ \]', content):
            validation_errors.append("No uncompleted todos found - task may already be complete")

        # Check for unfilled sections
        if "[To be filled by Claude]" in content or "[To be updated" in content:
            validation_errors.append("Plan contains unfilled sections")

        # Check for implementation steps
        if "## Implementation Steps" not in content and "### Implementation Steps" not in content and "## Detailed Steps" not in content:
            validation_errors.append("Missing implementation steps")

    except Exception as e:
        validation_errors.append(f"Error reading task file: {e}")

    return validation_errors


def main():
    # Read hook input
    hook_data = json.loads(sys.stdin.read())
    user_input = hook_data.get('input', '')

    if user_input.startswith('/brandifai:task-exec '):
        # Raw text format: /brandifai:task-exec task-name
        is_brandifai_task_exec = True
        task_file_pattern = user_input[21:].strip()
    elif '<command-name>/brandifai:task-exec</command-name>' in user_input:
        # XML format from Claude Code UI
        is_brandifai_task_exec = True
        # Extract command args from XML
        import re
        args_match = re.search(r'<command-args>(.*?)</command-args>', user_input, re.DOTALL)
        if args_match:
            task_file_pattern = args_match.group(1).strip()

    if is_brandifai_task_exec:
        # Check if input is empty
        if not task_file_pattern:
            error_msg = """ERROR: Invalid usage of /brandifai:task-exec command.

Correct usage: /brandifai:task-exec task-name-slug

Examples:
  /brandifai:task-exec user-auth
  /brandifai:task-exec payment-integration
  /brandifai:task-exec api-endpoints

The task-name-slug should match a previously planned task file."""

            result = {
                "input": error_msg,
                "continue": False
            }
            print(json.dumps(result))
            return

        # Find the task file
        task_file = None

        # If it's a full path, use it directly
        if task_file_pattern.startswith('.claude/tasks/') and task_file_pattern.endswith('.md'):
            if os.path.exists(task_file_pattern):
                task_file = task_file_pattern
        else:
            # Search for matching task files
            search_patterns = [
                f".claude/tasks/*{task_file_pattern}*.md",
                f".claude/tasks/*{task_file_pattern.replace(' ', '-')}*.md",
                f".claude/tasks/*{task_file_pattern.replace(' ', '_')}*.md"
            ]

            for pattern in search_patterns:
                matches = glob.glob(pattern)
                if matches:
                    # Use the most recent match
                    task_file = max(matches, key=os.path.getctime)
                    break

        if task_file:
            print(f"Found task file: {task_file}")

            # Check task status
            status = check_task_status(task_file)
            if status == "completed":
                result = {
                    "input": f"Task {task_file} is already marked as COMPLETED. If you want to re-execute, please update the Final Status section first.",
                    "continue": False
                }
                print(json.dumps(result))
                return
            elif status == "failed":
                print(f"Warning: Task previously failed. Retrying execution...")
            elif status == "blocked":
                result = {
                    "input": f"Task {task_file} is marked as BLOCKED. Please resolve blocking issues before execution.",
                    "continue": False
                }
                print(json.dumps(result))
                return

            # Validate task is ready for execution
            validation_errors = validate_task_ready(task_file)
            if validation_errors:
                error_msg = f"""Task file not ready for execution:
{chr(10).join('- ' + err for err in validation_errors)}

Please run: /brandifai:task-plan {task_file_pattern} to complete the planning phase."""
                result = {
                    "input": error_msg,
                    "continue": False
                }
                print(json.dumps(result))
                return

            # Get execution strategy based on complexity
            strategy = get_execution_strategy(task_file)

            # Create structured execution instructions
            progress_template = """When updating the task file progress log, use this format:
### {timestamp} - {Phase Name}
- Action: {what was done}
- Files: {files created/modified with full paths}
- Result: {success/failure/partial}
- Notes: {any issues or deviations from plan}
- Time taken: {duration}"""

            error_handling = """ERROR HANDLING PROTOCOL:
1. Compilation/Syntax errors: Fix immediately, document fix in log
2. Missing dependencies: Add to package.json/pom.xml/requirements.txt, re-run install
3. Test failures: Fix if simple, otherwise document and continue
4. File not found: Verify path, create parent directories if needed
5. Permission denied: Document issue, suggest chmod/sudo fix"""

            completion_checklist = """BEFORE MARKING TASK COMPLETE:
□ All todos marked as done [x]
□ All files in plan created/modified
□ Tests written and passing
□ Lint/build commands successful
□ Progress log fully updated with timestamps
□ No unresolved errors documented
□ Code follows existing patterns from codebase
□ Documentation updated if specified in plan"""

            execution_instructions = f"""TASK EXECUTION STARTED
File: {task_file}
Complexity Strategy: {strategy['strategy']}
Validation Level: {strategy['validation_level']}

=== EXECUTION INSTRUCTIONS ===

1. **FIRST: Read the entire plan** in {task_file}
2. **Use TodoWrite tool** to load ALL todos from the plan
3. **Follow the File Modifications Table** with exact paths and line numbers
4. **Update task file progress** using Edit tool after EACH major step
5. **Mark todos as completed** in real-time: change [ ] to [x] using Edit
6. **Run tests** after implementation if specified
7. **Document ANY deviations** from the plan

=== EXECUTION PHASES ===
Phase 1: Setup - Create new files, add dependencies
Phase 2: Implementation - Modify existing files per plan
Phase 3: Testing - Run tests, fix issues
Phase 4: Validation - Run lint/build, verify all changes

=== PROGRESS TRACKING ===
{progress_template}

=== ERROR HANDLING ===
{error_handling}

=== CRITICAL REQUIREMENTS ===
- Use EXACT file paths and line numbers from the plan
- Use code snippets provided in the plan
- Update progress log with timestamps after each phase
- Handle errors gracefully and document them
- Run lint/build/test commands after changes
- If using agents: Use Task tool for complex subtasks

=== COMPLETION CHECKLIST ===
{completion_checklist}

Now execute the task from: {task_file}"""

            result = {
                "input": execution_instructions,
                "continue": True
            }
        else:
            # Task file not found - list available tasks
            available_tasks = glob.glob(".claude/tasks/*.md")
            task_list = ""
            if available_tasks:
                task_list = "\n\nAvailable task files (showing last 10):\n"
                for task in sorted(available_tasks)[-10:]:
                    task_name = os.path.basename(task)
                    # Try to get task status
                    status = check_task_status(task)
                    status_indicator = ""
                    if status == "completed":
                        status_indicator = " [COMPLETED]"
                    elif status == "failed":
                        status_indicator = " [FAILED]"
                    elif status == "blocked":
                        status_indicator = " [BLOCKED]"
                    elif status == "likely_completed":
                        status_indicator = " [LIKELY COMPLETE]"
                    task_list += f"  - {task_name}{status_indicator}\n"

            error_msg = f"""ERROR: Task file not found for: {task_file_pattern}{task_list}

Please ensure:
1. You've created the task using: /brandifai:task "Task Name" description
2. You've planned the task using: /brandifai:task-plan {task_file_pattern}
3. The task-name-slug matches the task file name

Example workflow:
  /brandifai:task "User Auth" Implement JWT authentication
  /brandifai:task-plan user-auth
  /brandifai:task-exec user-auth"""

            result = {
                "input": error_msg,
                "continue": False
            }
            print(f"Task file not found for pattern: {task_file_pattern}")

        print(json.dumps(result))
    else:
        # Pass through unchanged
        result = {
            "input": user_input,
            "continue": True
        }
        print(json.dumps(result))


if __name__ == "__main__":
    main()
