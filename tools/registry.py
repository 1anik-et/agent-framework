from tools.file_ops import write_workspace_file, read_workspace_file, edit_workspace_file, delete_workspace_file, list_workspace_files
from tools.terminal import run_terminal_command

# 1. Map string names directly to executable python functions
TOOL_MAP = {
    "write_workspace_file": write_workspace_file,
    "read_workspace_file": read_workspace_file,
    "edit_workspace_file": edit_workspace_file,
    "delete_workspace_file": delete_workspace_file,
    "list_workspace_files": list_workspace_files,
    "run_terminal_command": run_terminal_command
}

# 2. Define standard JSON schemas that the Groq model reads
GROQ_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "write_workspace_file",
            "description": "Create a new file or overwrite an existing file inside the workspace with specified code or text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the file (e.g., 'linked_list.cpp' or 'server.js')."
                    },
                    "content": {
                        "type": "string",
                        "description": "The full code content to be written inside the file."
                    }
                },
                "required": ["filename", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_workspace_file",
            "description": "Read and return the complete code contents of an existing file inside the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The target filename to look up."
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_workspace_file",
            "description": "Edits an existing file in the workspace by replacing an exact string match with new text. Think of this like a targeted search and replace or a unified diff block.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The target filename to modify."
                    },
                    "search_content": {
                        "type": "string",
                        "description": "The exact multi-line string block currently in the file that you want to replace. Must be unique within the file."
                    },
                    "replace_content": {
                        "type": "string",
                        "description": "The new multi-line string block to replace the search_content with."
                    }
                },
                "required": ["filename", "search_content", "replace_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_workspace_file",
            "description": "Deletes an existing file from the workspace. Use the exact filename from list_workspace_files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The exact target filename to delete. Use the name returned by list_workspace_files."
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_workspace_files",
            "description": "Lists all files and folders currently in the workspace. ALWAYS call this first when you need to find, edit, or delete a file so you know the exact filenames.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory_path": {
                        "type": "string",
                        "description": "The directory path to list files from. Use '.' for the root workspace directory."
                    }
                },
                "required": ["directory_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_terminal_command",
            "description": "Executes a whitelisted terminal command inside the workspace sandbox. Use this to compile code, run scripts, execute tests, or install packages. If the output contains errors, you can read the file, fix it with edit_workspace_file, and run the command again.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to execute (e.g., 'python test.py', 'gcc main.c -o main', 'node server.js')."
                    }
                },
                "required": ["command"]
            }
        }
    }
]