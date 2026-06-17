import os
from config import WORKSPACE_DIR

def write_workspace_file(filename: str, content: str) -> str:
    """Creates or overwrites a file inside the localized agent workspace."""
    try:
        # THE FIX: normpath cleans the string. We block absolute paths and upward traversals (..)
        clean_path = os.path.normpath(filename)
        if clean_path.startswith("/") or clean_path.startswith("\\") or clean_path.startswith(".."):
            return "Error: Invalid filename. You cannot use absolute paths or traverse outside the workspace."
            
        filepath = os.path.join(WORKSPACE_DIR, clean_path)
        
        # Ensure any sub-folders (like backend/src/) are generated automatically
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"Success: Written {len(content)} characters to '{clean_path}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"
    
def read_workspace_file(filename: str) -> str:
    """Reads the text content of a specific file inside the workspace."""
    try:
        clean_path = os.path.normpath(filename)
        if clean_path.startswith("/") or clean_path.startswith("\\") or clean_path.startswith(".."):
            return "Error: Invalid filename."
            
        filepath = os.path.join(WORKSPACE_DIR, clean_path)
        
        if not os.path.exists(filepath):
            return f"Error: File '{clean_path}' does not exist in workspace."
        
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def edit_workspace_file(filename: str, search_content: str, replace_content: str) -> str:
    """Edits a file by replacing an exact string match (search_content) with new text (replace_content)."""
    try:
        clean_path = os.path.normpath(filename)
        if clean_path.startswith("/") or clean_path.startswith("\\") or clean_path.startswith(".."):
            return "Error: Invalid filename."
            
        filepath = os.path.join(WORKSPACE_DIR, clean_path)
        
        if not os.path.exists(filepath):
            return f"Error: File '{clean_path}' does not exist in workspace."
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        if search_content not in content:
            return f"Error: The exact search_content block was not found in '{clean_path}'."
            
        if content.count(search_content) > 1:
            return f"Error: The search_content matched multiple locations. Please provide a more specific search block."
            
        new_content = content.replace(search_content, replace_content)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        return f"Success: Replaced targeted content in '{clean_path}'."
    except Exception as e:
        return f"Error editing file: {str(e)}"

def delete_workspace_file(filename: str) -> str:
    """Deletes an existing file inside the workspace."""
    try:
        clean_path = os.path.normpath(filename)
        if clean_path.startswith("/") or clean_path.startswith("\\") or clean_path.startswith(".."):
            return "Error: Invalid filename."
            
        filepath = os.path.join(WORKSPACE_DIR, clean_path)
        
        if not os.path.exists(filepath):
            return f"Error: File '{clean_path}' does not exist in workspace."
            
        os.remove(filepath)
        return f"Success: Deleted '{clean_path}'."
    except Exception as e:
        return f"Error deleting file: {str(e)}"

def list_workspace_files(**kwargs) -> str:
    """Lists all files and folders in the workspace directory recursively."""
    try:
        file_list = []
        for root, dirs, files in os.walk(WORKSPACE_DIR):
            # Get the relative path from workspace root
            rel_root = os.path.relpath(root, WORKSPACE_DIR)
            for f in files:
                if rel_root == ".":
                    file_list.append(f)
                else:
                    file_list.append(os.path.join(rel_root, f))
        
        if not file_list:
            return "The workspace is empty. No files found."
        
        return "Files in workspace:\n" + "\n".join(f"  - {f}" for f in sorted(file_list))
    except Exception as e:
        return f"Error listing files: {str(e)}"
