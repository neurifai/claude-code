#!/usr/bin/env python3
import json
import sys
import os

def main():
    # Read hook input
    hook_data = json.loads(sys.stdin.read())
    user_input = hook_data.get('input', '')

    if user_input.startswith('/brandifai:help'):
        command_arg = user_input[15:].strip()  # Remove '/brandifai:help'
        
        if command_arg:
            # Show help for specific command
            # Handle both with and without namespace prefix
            if command_arg.startswith('brandifai:'):
                command_arg = command_arg[10:]  # Remove 'brandifai:' prefix
            doc_file = f".claude/commands/brandifai/{command_arg}.md"
            if os.path.exists(doc_file):
                with open(doc_file, 'r') as f:
                    content = f.read()
                print(f"Help for /brandifai:{command_arg}:")
                print("=" * 50)
                print(content)
            else:
                print(f"ERROR: No help available for command: /brandifai:{command_arg}")
                print("\nAvailable commands:")
                commands_dir = ".claude/commands/brandifai"
                if os.path.exists(commands_dir):
                    md_files = [f[:-3] for f in os.listdir(commands_dir) if f.endswith('.md')]
                    for cmd in md_files:
                        print(f"  /brandifai:{cmd}")
                print("\nUse '/brandifai:help' to see all available commands")
        else:
            # Show available commands
            commands_dir = ".claude/commands/brandifai"
            if os.path.exists(commands_dir):
                md_files = [f[:-3] for f in os.listdir(commands_dir) if f.endswith('.md')]
                if md_files:
                    print("Available custom commands:")
                    print("=" * 30)
                    for cmd in md_files:
                        print(f"/brandifai:{cmd}")
                    print("\nUse '/brandifai:help <command>' for detailed help on a specific command")
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