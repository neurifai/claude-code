#!/usr/bin/env python3
import json
import sys
import os
from datetime import datetime
import re


def assess_task_complexity(task_description):
    """
    Assess task complexity based on keywords and patterns in the description.
    Returns: 'easy', 'medium', or 'hard'
    """
    description_lower = task_description.lower()

    # Hard complexity indicators
    hard_indicators = [
        'backend', 'api', 'database', 'architecture', 'system', 'integration',
        'authentication', 'authorization', 'security', 'scalable', 'distributed',
        'microservice', 'crud', 'rest api', 'graphql', 'websocket', 'real-time',
        'async', 'concurrent', 'multi-threaded', 'performance', 'optimization',
        'deployment', 'devops', 'infrastructure', 'cloud', 'kubernetes', 'docker',
        'testing framework', 'ci/cd', 'pipeline', 'monitoring', 'logging',
        'error handling', 'validation', 'encryption', 'payment', 'billing',
        'notification system', 'email service', 'file upload', 'media processing',
        'search engine', 'indexing', 'caching', 'redis', 'elasticsearch',
        'machine learning', 'ai model', 'neural network', 'data processing',
        'lambda', 'dynamodb', 'service layer', 'multi-tenant', 'scheduler'
    ]

    # Medium complexity indicators
    medium_indicators = [
        'component', 'service', 'class', 'module', 'library', 'framework',
        'ui component', 'form validation', 'data transformation', 'parsing',
        'configuration', 'settings', 'workflow', 'process', 'algorithm',
        'data structure', 'sorting', 'filtering', 'search', 'pagination',
        'routing', 'navigation', 'state management', 'event handling',
        'refactor', 'refactoring', 'restructure', 'organize', 'cleanup',
        'multiple files', 'several', 'various', 'different', 'complex'
    ]

    # Easy complexity indicators (or lack of complexity indicators)
    easy_indicators = [
        'simple', 'basic', 'quick', 'small', 'minor', 'trivial', 'easy',
        'single', 'one', 'fix bug', 'update', 'change', 'modify', 'add comment',
        'rename', 'format', 'style', 'color', 'text', 'label', 'title'
    ]

    # Count indicators
    hard_count = sum(1 for indicator in hard_indicators if indicator in description_lower)
    medium_count = sum(1 for indicator in medium_indicators if indicator in description_lower)
    easy_count = sum(1 for indicator in easy_indicators if indicator in description_lower)

    # Check for multiple steps/requirements (numbered lists)
    numbered_steps = len(re.findall(r'\d+\.', task_description))
    bullet_points = len(re.findall(r'[-*•]', task_description))

    # Decision logic
    if hard_count >= 2 or numbered_steps >= 4 or bullet_points >= 5:
        return 'hard'
    elif hard_count >= 1 or medium_count >= 2 or numbered_steps >= 2 or bullet_points >= 3:
        return 'medium'
    elif easy_count >= 1 and hard_count == 0 and medium_count <= 1:
        return 'easy'
    else:
        # Default to medium for ambiguous cases
        return 'medium'


def main():
    # Read hook input
    hook_data = json.loads(sys.stdin.read())
    user_input = hook_data.get('input', '')

    if user_input.startswith('/brandifai:task '):
        task_input = user_input[16:].strip()  # Remove '/brandifai:task '
        
        # Check if input is empty
        if not task_input:
            error_msg = """ERROR: Invalid usage of /brandifai:task command.

Correct usage: /brandifai:task "Task Name" detailed description

Examples:
  /brandifai:task "User Auth" Implement JWT-based authentication with refresh tokens
  /brandifai:task "Payment Integration" Add Stripe payment processing with webhook handling
  
The task name should be in quotes, followed by a detailed description."""
            
            result = {
                "input": error_msg,
                "continue": False
            }
            print(json.dumps(result))
            return

        # Parse task name and description
        if task_input.startswith('"'):
            # Find the closing quote
            end_quote = task_input.find('"', 1)
            if end_quote != -1:
                task_name_raw = task_input[1:end_quote]
                task_description = task_input[end_quote + 1:].strip()
                
                # Validate that we have both name and description
                if not task_name_raw:
                    error_msg = """ERROR: Task name cannot be empty.

Correct usage: /brandifai:task "Task Name" detailed description"""
                    result = {
                        "input": error_msg,
                        "continue": False
                    }
                    print(json.dumps(result))
                    return
                    
                if not task_description:
                    error_msg = """ERROR: Task description is required.

Correct usage: /brandifai:task "Task Name" detailed description

Example: /brandifai:task "User Auth" Implement JWT-based authentication with refresh tokens"""
                    result = {
                        "input": error_msg,
                        "continue": False
                    }
                    print(json.dumps(result))
                    return
            else:
                # No closing quote found
                error_msg = """ERROR: Task name must be enclosed in quotes.

Correct usage: /brandifai:task "Task Name" detailed description

Example: /brandifai:task "User Auth" Implement JWT-based authentication with refresh tokens"""
                result = {
                    "input": error_msg,
                    "continue": False
                }
                print(json.dumps(result))
                return
        else:
            # No quotes, treat entire input as description (backward compatibility)
            task_name_raw = task_input
            task_description = task_input

        # Assess task complexity
        complexity = assess_task_complexity(task_description)

        # Create task file
        task_name = task_name_raw.lower().replace(' ', '-')[:50]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f".claude/tasks/{timestamp}_{task_name}.md"

        try:
            os.makedirs('.claude/tasks', exist_ok=True)

            # Create the task file content
            task_content = f"""# Task: {task_name_raw}

## Overview
{task_description}

## Complexity Assessment
**Assessed Complexity:** {complexity.upper()}

## Execution Plan
[To be filled by Claude]

## Todo List
- [ ] Plan implementation approach
- [ ] Begin execution

## Progress Log
### {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Task created via /brandifai:task command
- Complexity assessed as: {complexity}

## Changes Made
[To be updated during implementation]

## Issues Encountered
[To be documented as they arise]

## Final Status
[To be completed when task is finished]
"""

            # Write the file with explicit flushing and syncing
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(task_content)
                f.flush()
                os.fsync(f.fileno())

            # Verify the file was created
            if not os.path.exists(filename):
                raise Exception(f"File was not created: {filename}")

        except Exception as e:
            print(f"Error creating task file: {e}")
            result = {
                "input": f"Error creating task file: {e}",
                "continue": True
            }
            print(json.dumps(result))
            return

        # Output for Claude to see
        print(f"SUCCESS: Created task file: {filename}")
        print(f"Task: {task_description}")
        print(f"Assessed complexity: {complexity}")
        print(f"File exists: {os.path.exists(filename)}")
        print(f"File size: {os.path.getsize(filename) if os.path.exists(filename) else 'N/A'} bytes")

        # Just acknowledge task creation, no planning
        new_input = f"Task file created successfully at {filename}. You can now manually edit the file to add more context if needed, then use '/brandifai:task-plan {task_name}' to create the execution plan."

        # Return modified input
        result = {
            "input": new_input,
            "continue": True
        }
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
