import subprocess
import os
import re

SCRIPT_FILE = os.path.abspath("run_command.sh")  # Get absolute path

def extract_command(response):
    """
    Extracts only the command from GPT-4o's response, filtering out extra text.
    Assumes the command is in a code block or appears as the last line.
    """
    # Check for a fenced code block (```bash ... ```)
    match = re.search(r"```(?:bash)?\s*([\s\S]*?)\s*```", response)
    if match:
        return match.group(1).strip()

    # If no fenced block, take the last line as the command
    lines = response.strip().split("\n")
    return lines[-1].strip()

def write_and_execute_command(response):
    """Writes the extracted command to a script file and executes it interactively in a new macOS Terminal window."""

    command = extract_command(response)  # Extract only the shell command

    if not command or " " not in command:  # Basic check to ensure valid command
        print("Error: Could not extract a valid command.")
        return

    # Write the command to the script file
    with open(SCRIPT_FILE, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("exec " + command + "\n")  # `exec` ensures the SSH session takes over

    # Make the script executable
    subprocess.run(["chmod", "+x", SCRIPT_FILE])

    # Open the script in a new terminal window and execute it directly
    apple_script = f'''
    tell application "Terminal"
        do script "{command}"
        activate
    end tell
    '''
    subprocess.run(["osascript", "-e", apple_script])

if __name__ == "__main__":
    response = input("Enter the AI-generated response: ")
    write_and_execute_command(response)
