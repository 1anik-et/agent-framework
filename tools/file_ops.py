import os
from config import WORKSPACE_DIR

def write_workspace_file(filename: str, content: str) -> str:
    """Creates or overwrites a file inside the localized agent workspace."""
    try:
        os.makedirs(WORKSPACE_DIR, exist_ok=True)
        filepath = os.path.join(WORKSPACE_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Success: Written {len(content)} characters to '{filename}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"
    
def read_workspace_file(filename: str) -> str:
    """Reads the text content of a specific file inside the workspace."""
    try:
        filepath = os.path.join(WORKSPACE_DIR, filename)
        if not os.path.exists(filepath):
            return f"Error: File '{filename}' does not exist."
        
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"