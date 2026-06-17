import subprocess
import os
from config import WORKSPACE_DIR

# Whitelist of safe commands the agent is allowed to execute
ALLOWED_COMMANDS = [
    "python", "python3", "node", "npm", "gcc", "g++", "javac", "java",
    "pip", "pip3", "cat", "echo", "ls", "dir", "type", "mkdir",
    "pytest", "cargo", "rustc", "go", "dotnet"
]

def run_terminal_command(command: str) -> str:
    """
    Executes a whitelisted terminal command inside the workspace sandbox.
    Returns stdout + stderr combined. Enforces a timeout to prevent infinite hangs.
    """
    try:
        # Extract the base command (first word) for whitelist check
        base_command = command.strip().split()[0].lower()
        
        # Strip dangerous path prefixes from the base command
        base_command = os.path.basename(base_command)
        
        if base_command not in ALLOWED_COMMANDS:
            return f"Error: Command '{base_command}' is not whitelisted. Allowed commands: {', '.join(ALLOWED_COMMANDS)}"
        
        # Block dangerous shell patterns
        dangerous_patterns = ["&&", "||", ";", "|", ">", "<", "`", "$(", "rm ", "del ", "rmdir", "format"]
        for pattern in dangerous_patterns:
            if pattern in command:
                return f"Error: Command contains blocked pattern '{pattern}'. Only simple, single commands are allowed."
        
        # Execute inside the workspace directory with a timeout
        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
            errors="replace"
        )
        
        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}"
        
        if result.returncode != 0:
            output += f"\n[EXIT CODE: {result.returncode}]"
        else:
            output += f"\n[EXIT CODE: 0 - Success]"
            
        return output.strip() if output.strip() else "[No output produced]"
        
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error running command: {str(e)}"
