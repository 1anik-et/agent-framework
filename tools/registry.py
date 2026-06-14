from tools.file_ops import write_workspace_file, read_workspace_file

# 1. Map string names directly to executable python functions
TOOL_MAP = {
    "write_workspace_file": write_workspace_file,
    "read_workspace_file": read_workspace_file
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
    }
]