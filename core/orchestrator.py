import json
from groq import Groq
from typing import List, Dict, Any

class Orchestrator:
    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.system_prompt = (
            "You are an expert Software Architect and Project Manager.\n"
            "Your job is to break down a complex user request into a sequence of small, independent, actionable sub-tasks.\n"
            "\n"
            "The worker agent has ONLY these tools:\n"
            "  - `list_workspace_files(directory_path)`: Lists all files in the workspace.\n"
            "  - `read_workspace_file(filename)`: Reads a file's contents.\n"
            "  - `write_workspace_file(filename, content)`: Creates or overwrites a file.\n"
            "  - `edit_workspace_file(filename, search_content, replace_content)`: Surgically edits part of a file.\n"
            "  - `delete_workspace_file(filename)`: Deletes a file.\n"
            "  - `run_terminal_command(command)`: Runs a terminal command (e.g., python, gcc, node, pytest).\n"
            "\n"
            "CRITICAL RULES FOR TASK DECOMPOSITION:\n"
            "1. NEVER create tasks the worker cannot do (e.g., 'navigate directory', 'check permissions', 'open editor'). Only plan tasks that use the tools above.\n"
            "2. Keep tasks minimal. A simple request like 'delete a file' should be 1-2 tasks max, NOT 5.\n"
            "3. If the user references a file vaguely (e.g., 'the gibberish file'), the FIRST task should always be: 'List workspace files to identify the target.'\n"
            "4. Each task description must be concrete enough to execute with the tools listed.\n"
            "5. When the user asks to write code, include a FINAL task to run/compile/test it using `run_terminal_command`. If errors appear, the worker will self-heal by reading the error, fixing the code, and re-running.\n"
            "\n"
            "Provide the output strictly as a JSON object containing a list under the key 'tasks'.\n"
            "Do not include any conversational text or markdown code blocks outside the JSON."
        )
        
    def plan(self, user_goal: str) -> List[Dict[str, Any]]:
        prompt = (
            f"User Goal: {user_goal}\n\n"
            "Decompose this goal into a sequential list of steps. "
            "Each task must contain an 'id' (integer), a 'title', and a detailed 'description'."
        )
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        raw_content = response.choices[0].message.content
        data = json.loads(raw_content)
        return data.get("tasks", [])