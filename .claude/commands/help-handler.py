#!/usr/bin/env python3
import json
import sys
import os

def main():
    # Read hook input
    hook_data = json.loads(sys.stdin.read())
    user_input = hook_data.get('input', '')

    if user_input.startswith('/help'):
        command_arg = user_input[5:].strip()  # Remove '/help'
        
        if command_arg:
            # Show help for specific command
            doc_file = f".claude/commands/{command_arg}.md"
            if os.path.exists(doc_file):
                with open(doc_file, 'r') as f:
                    content = f.read()
                print(f"Help for /{command_arg}:")
                print("=" * 50)
                print(content)
            else:
                print(f"No help available for command: /{command_arg}")
        else:
            # Show available commands
            commands_dir = ".claude/commands"
            if os.path.exists(commands_dir):
                md_files = [f[:-3] for f in os.listdir(commands_dir) if f.endswith('.md')]
                if md_files:
                    print("Available custom commands:")
                    print("=" * 30)
                    for cmd in md_files:
                        print(f"/{cmd}")
                    print("\nUse '/help <command>' for detailed help on a specific command")
                else:
                    print("No custom commands found")
            else:
                print("No custom commands directory found")
        
        # Return empty input to prevent further processing
        result = {
            "input": "",
            "continue": False
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