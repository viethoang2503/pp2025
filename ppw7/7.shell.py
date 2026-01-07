#!/usr/bin/env python3
"""
Practical Work 7: Python Shell
A simple shell that supports:
- User input commands
- Command execution with output
- IO redirection (input from file, output to file, piping)
"""

import subprocess
import sys
import os
import shlex


class PyShell:
    def __init__(self):
        self.running = True
        
    def parse_command(self, cmd_line):
        """Parse command line for IO redirection"""
        # Check for output redirection (>)
        if '>' in cmd_line:
            parts = cmd_line.split('>', 1)
            command = parts[0].strip()
            output_file = parts[1].strip()
            return command, None, output_file, None
        
        # Check for input redirection (<)
        elif '<' in cmd_line:
            parts = cmd_line.split('<', 1)
            command = parts[0].strip()
            input_file = parts[1].strip()
            return command, input_file, None, None
        
        # Check for pipe (|)
        elif '|' in cmd_line:
            parts = cmd_line.split('|')
            cmd1 = parts[0].strip()
            cmd2 = parts[1].strip() if len(parts) > 1 else None
            return cmd1, None, None, cmd2
        
        else:
            return cmd_line.strip(), None, None, None
    
    def execute_command(self, command, input_file=None, output_file=None, pipe_to=None):
        """Execute a command with optional IO redirection"""
        try:
            # Handle built-in commands
            if command.startswith('cd '):
                path = command[3:].strip()
                try:
                    os.chdir(path)
                    print(f"Changed directory to: {os.getcwd()}")
                except FileNotFoundError:
                    print(f"Error: Directory '{path}' not found")
                return
            
            elif command == 'pwd':
                print(os.getcwd())
                return
            
            elif command in ['exit', 'quit']:
                self.running = False
                print("Goodbye!")
                return
            
            # Parse command arguments
            try:
                args = shlex.split(command)
            except ValueError as e:
                print(f"Error parsing command: {e}")
                return
            
            # Handle input redirection (<)
            stdin_data = None
            if input_file:
                try:
                    with open(input_file, 'r') as f:
                        stdin_data = f.read()
                except FileNotFoundError:
                    print(f"Error: Input file '{input_file}' not found")
                    return
                except Exception as e:
                    print(f"Error reading input file: {e}")
                    return
            
            # Execute command
            if pipe_to:
                # Handle piping (|)
                try:
                    # Execute first command
                    proc1 = subprocess.Popen(
                        args,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    # Execute second command with output from first
                    args2 = shlex.split(pipe_to)
                    proc2 = subprocess.Popen(
                        args2,
                        stdin=proc1.stdout,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    proc1.stdout.close()
                    output, error = proc2.communicate()
                    
                    if output:
                        print(output, end='')
                    if error:
                        print(f"Error: {error}", file=sys.stderr)
                        
                except FileNotFoundError:
                    print(f"Error: Command not found")
                except Exception as e:
                    print(f"Error executing piped command: {e}")
                    
            elif output_file:
                # Handle output redirection (>)
                try:
                    result = subprocess.run(
                        args,
                        input=stdin_data,
                        capture_output=True,
                        text=True
                    )
                    
                    # Write output to file
                    with open(output_file, 'w') as f:
                        f.write(result.stdout)
                    
                    print(f"Output written to '{output_file}'")
                    
                    if result.stderr:
                        print(f"Error: {result.stderr}", file=sys.stderr)
                        
                except FileNotFoundError:
                    print(f"Error: Command '{args[0]}' not found")
                except Exception as e:
                    print(f"Error executing command: {e}")
                    
            else:
                # Normal execution
                try:
                    result = subprocess.run(
                        args,
                        input=stdin_data,
                        capture_output=True,
                        text=True
                    )
                    
                    if result.stdout:
                        print(result.stdout, end='')
                    if result.stderr:
                        print(result.stderr, end='', file=sys.stderr)
                        
                except FileNotFoundError:
                    print(f"Error: Command '{args[0]}' not found")
                except Exception as e:
                    print(f"Error executing command: {e}")
                    
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def run(self):
        """Main shell loop"""
        print("=" * 50)
        print("Python Shell - Practical Work 7")
        print("=" * 50)
        print("Type 'exit' or 'quit' to exit the shell")
        print("Supports: <, >, | for IO redirection")
        print()
        
        while self.running:
            try:
                # Display prompt
                prompt = f"{os.getcwd()} $ "
                cmd_line = input(prompt)
                
                # Skip empty commands
                if not cmd_line.strip():
                    continue
                
                # Parse and execute command
                command, input_file, output_file, pipe_to = self.parse_command(cmd_line)
                self.execute_command(command, input_file, output_file, pipe_to)
                
            except KeyboardInterrupt:
                print("\nUse 'exit' or 'quit' to exit the shell")
            except EOFError:
                print("\nGoodbye!")
                break


def main():
    shell = PyShell()
    shell.run()


if __name__ == "__main__":
    main()
