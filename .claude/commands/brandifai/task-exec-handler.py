#!/usr/bin/env python3
import json
import sys
import os
import glob

def main():
    # Read hook input
    hook_data = json.loads(sys.stdin.read())
    user_input = hook_data.get('input', '')

    if user_input.startswith('/brandifai:task-exec '):
        task_file_pattern = user_input[21:].strip()  # Remove '/brandifai:task-exec '
        
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
            # Modify the input to tell Claude to execute the task
            new_input = f"Please execute the task plan in the file {task_file}. Follow the execution plan and todos specified in that file."
            
            result = {
                "input": new_input,
                "continue": True
            }
            print(f"Found task file: {task_file}")
        else:
            # Task file not found
            error_msg = f"""ERROR: Task file not found for: {task_file_pattern}

Please ensure:
1. You've created the task using: /brandifai:task "Task Name" description
2. You've planned the task using: /brandifai:task-plan {task_file_pattern}
3. The task-name-slug matches the task file name

Use /brandifai:help task-exec for more information."""
            
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