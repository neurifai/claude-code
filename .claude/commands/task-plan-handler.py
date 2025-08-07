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

  if user_input.startswith('/task-plan '):
    task_name_slug = user_input[11:].strip()  # Remove '/task-plan '
    
    if not task_name_slug:
      print("Error: Please provide a task name")
      result = {
        "input": "Error: Please provide a task name for /task-plan command",
        "continue": True
      }
      print(json.dumps(result))
      return

    # Find the task file by name
    task_files = glob.glob(f".claude/tasks/*_{task_name_slug}.md")
    
    if not task_files:
      print(f"Error: No task file found for '{task_name_slug}'")
      result = {
        "input": f"Error: No task file found for '{task_name_slug}'. Use '/task' to create it first.",
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

    # Output for Claude to see
    print(f"Found task file: {task_file}")
    print(f"Complexity: {complexity}")
    print(f"Description: {task_description}")

    # Create detailed planning instruction with strict constraints
    if complexity in ['medium', 'hard']:
        thinking_instruction = " Use <claude:thinking> tags to work through the complexity and design decisions."
    else:
        thinking_instruction = ""
    
    constraints = """
CRITICAL CONSTRAINTS FOR TASK PLANNING:
- This is a PLANNING-ONLY phase. You must NOT execute any code changes.
- ALLOWED tools: Read, Grep, Glob, LS (research only), TodoWrite (task management), Edit (ONLY for updating the task file itself)
- PROHIBITED tools: Write (new files), Edit (code files), Bash (implementation), MultiEdit
- You MUST stop after creating the detailed plan and explicitly state "Task planning complete - ready for execution phase"
- Do NOT create, modify, or delete any code files during planning
- Do NOT use implementation tools like Write, MultiEdit, or Bash commands"""
    
    new_input = f"I found the task file at {task_file}. Please analyze this task and create a detailed execution plan with specific todos.{thinking_instruction} Follow the existing fueler-server architecture patterns: Lambda handlers extend Base classes, services take DynamoDbHelper as constructor dependency, no repository layer. Update the task file with your execution plan, then STOP.{constraints} Task: {task_description}"

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