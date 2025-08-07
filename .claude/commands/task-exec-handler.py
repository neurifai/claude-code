#!/usr/bin/env python3
import json
import sys
import os
import glob

def main():
    # Read hook input
    hook_data = json.loads(sys.stdin.read())
    user_input = hook_data.get('input', '')

    if user_input.startswith('/task-exec '):
        task_file_pattern = user_input[11:].strip()  # Remove '/task-exec '
        
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
            new_input = f"Task file not found for pattern: {task_file_pattern}. Please check the file name or use /help task-exec for usage instructions."
            
            result = {
                "input": new_input,
                "continue": True
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