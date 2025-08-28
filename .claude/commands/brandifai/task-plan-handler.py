#!/usr/bin/env python3
import json
import sys
import os
import glob
from datetime import datetime

def main():
  # Read hook input
  hook_data = json.loads(sys.stdin.read())
  user_input = hook_data.get('input', '')

  if user_input.startswith('/brandifai:task-plan '):
    task_name_slug = user_input[21:].strip()  # Remove '/brandifai:task-plan '
    
    if not task_name_slug:
      error_msg = """ERROR: Invalid usage of /brandifai:task-plan command.

Correct usage: /brandifai:task-plan task-name-slug

Examples:
  /brandifai:task-plan user-auth
  /brandifai:task-plan payment-integration
  /brandifai:task-plan api-endpoints

The task-name-slug should match a previously created task file."""
      
      result = {
        "input": error_msg,
        "continue": False
      }
      print(json.dumps(result))
      return

    # Find the task file by name
    task_files = glob.glob(f".claude/tasks/*_{task_name_slug}.md")
    
    if not task_files:
      print(f"Error: No task file found for '{task_name_slug}'")
      result = {
        "input": f"Error: No task file found for '{task_name_slug}'. Use '/brandifai:task' to create it first.",
        "continue": True
      }
      print(json.dumps(result))
      return
    
    # Use the most recent file if multiple exist
    task_file = sorted(task_files)[-1]
    
    # Read the task file to get complexity and description
    try:
      with open(task_file, 'r') as f:
        content = f.read()
        
      # Extract complexity assessment
      complexity = 'medium'  # default
      if '**Assessed Complexity:** EASY' in content:
        complexity = 'easy'
      elif '**Assessed Complexity:** HARD' in content:
        complexity = 'hard'
      
      # Extract task description from overview section
      lines = content.split('\n')
      overview_start = -1
      overview_end = -1
      
      for i, line in enumerate(lines):
        if line.strip() == '## Overview':
          overview_start = i + 1
        elif overview_start > 0 and line.strip().startswith('##') and overview_start != i:
          overview_end = i
          break
      
      if overview_start > 0:
        if overview_end == -1:
          overview_end = len(lines)
        task_description = '\n'.join(lines[overview_start:overview_end]).strip()
      else:
        task_description = "Task description not found"
        
    except Exception as e:
      print(f"Error reading task file: {e}")
      result = {
        "input": f"Error reading task file {task_file}: {e}",
        "continue": True
      }
      print(json.dumps(result))
      return

    # Check for CLAUDE.md to determine architecture patterns
    architecture_context = ""
    if os.path.exists('CLAUDE.md'):
      try:
        with open('CLAUDE.md', 'r') as f:
          architecture_context = "Follow the architecture patterns defined in CLAUDE.md."
      except:
        architecture_context = "Analyze and follow the existing codebase patterns."
    else:
      architecture_context = "Analyze and follow the existing codebase patterns."
    
    # Output for Claude to see
    print(f"Found task file: {task_file}")
    print(f"Complexity: {complexity}")
    print(f"Description: {task_description}")

    # Create complexity-based analysis requirements
    if complexity == 'easy':
        analysis_depth = "Focus on: File locations, method signatures, basic error handling, simple test cases."
        thinking_instruction = ""
    elif complexity == 'medium':
        analysis_depth = "Include: Dependency analysis, integration points, data flow, state management, comprehensive error handling."
        thinking_instruction = " Use <claude:thinking> tags to work through the design decisions."
    else:  # hard
        analysis_depth = "Required: Architecture diagrams, sequence flows, security analysis, performance considerations, database schema changes, scalability concerns."
        thinking_instruction = " Use <claude:thinking> tags to thoroughly analyze the complex architectural decisions."
    
    # Create structured plan template
    plan_template = """
## Implementation Plan Structure

### 1. Prerequisites Check
- [ ] Dependencies and imports needed
- [ ] Files that will be modified (with line numbers)
- [ ] New files to be created

### 2. Implementation Steps
[Break down into numbered steps with specific file:line references]

### 3. File Modifications Table
| File Path | Change Type | Line Numbers | Description |
|-----------|-------------|--------------|-------------|
| [path]    | Edit/Create | [lines]      | [changes]   |

### 4. Code Patterns
[Include actual code snippets for complex parts]

### 5. Testing Checklist
- [ ] Unit tests for: [list specific functions]
- [ ] Integration tests for: [list integration points]
- [ ] Edge cases: [list edge cases to handle]

### 6. Rollback Plan
[Step-by-step instructions to undo changes if needed]
"""

    validation_checklist = """
PLAN VALIDATION CHECKLIST:
□ All file paths are absolute and verified to exist (or marked as NEW)
□ Line numbers provided for existing file modifications
□ Import statements are complete and exact
□ Function/method signatures include proper types
□ Database/API changes include migration steps
□ Error handling is explicitly planned
□ Test file locations and names are specified
□ Configuration changes are documented
"""
    
    constraints = """
CRITICAL CONSTRAINTS FOR TASK PLANNING:
- This is a PLANNING-ONLY phase. You must NOT execute any code changes.
- ALLOWED tools: Read, Grep, Glob, LS (research only), TodoWrite (task management), Edit (ONLY for updating the task file itself)
- PROHIBITED tools: Write (new files), Edit (code files), Bash (implementation), MultiEdit
- You MUST stop after creating the detailed plan and explicitly state "Task planning complete - ready for execution phase"
- Do NOT create, modify, or delete any code files during planning
- Do NOT use implementation tools like Write, MultiEdit, or Bash commands"""
    
    # Add required codebase analysis phase
    codebase_analysis = """
REQUIRED CODEBASE ANALYSIS:
Before planning, you MUST:
1. Identify existing patterns for similar features (use Grep/Glob)
2. Find and document exact import statements needed
3. Locate specific base classes/interfaces to extend
4. Document naming conventions (files, functions, variables)
5. Find configuration files that may need updates
6. Identify test file patterns and locations
"""
    
    new_input = f"""I found the task file at {task_file}.

{codebase_analysis}

{analysis_depth}

Please analyze this task and create a detailed execution plan following this structure:
{plan_template}

Ensure your plan meets these validation criteria:
{validation_checklist}

{thinking_instruction}

{architecture_context}

Update the task file with your detailed execution plan, then STOP.

{constraints}

Task: {task_description}"""

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