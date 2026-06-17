import json
from groq import Groq
from core.memory import MemoryManager
from tools.registry import GROQ_TOOLS, TOOL_MAP

class WorkerAgent:
    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.tools = GROQ_TOOLS
        self.tool_map = TOOL_MAP
        self.model = model
        
        # Use the MemoryManager for structured context tracking
        self.memory = MemoryManager(system_prompt=(
            "You are a strict, autonomous Software Engineer agent.\n"
            "You have these tools: `list_workspace_files`, `read_workspace_file`, `write_workspace_file`, "
            "`edit_workspace_file`, `delete_workspace_file`, `run_terminal_command`.\n"
            "\n"
            "CRITICAL RULES:\n"
            "1. When you need to find, edit, read, or delete a file, ALWAYS call `list_workspace_files` FIRST to discover the exact filenames. Never guess filenames.\n"
            "2. Use `edit_workspace_file` to modify specific parts of an existing file. Do NOT rewrite the entire file with `write_workspace_file` when only a small change is needed.\n"
            "3. Use `write_workspace_file` ONLY when creating a brand new file or completely replacing all content.\n"
            "4. Use `run_terminal_command` to compile, run, or test code. If the output contains errors, read the file, fix it with `edit_workspace_file`, and run the command again.\n"
            "5. DO NOT output raw code in markdown blocks in your chat response. Always use a tool.\n"
            "6. Only after you successfully trigger a tool should you summarize your work."
        ))

    def execute(self, task_description: str) -> str:
        # Add the task as a user message to the memory
        self.memory.add_message("user", f"Execute this micro-task: {task_description}")
        
        max_loops = 10
        current_loop = 0
        
        while current_loop < max_loops:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.memory.get_context(),
                    tools=self.tools,
                    tool_choice="auto"
                )
                
                message = response.choices[0].message
                # Append the raw assistant message to memory
                self.memory.messages.append(message)
                
                # Anti-Hallucination Lock
                # If it didn't call a tool on the very first loop, it is hallucinating text.
                if not message.tool_calls:
                    if current_loop == 0:
                        print("      [!] AI failed to use a tool. Forcing it to use a tool...")
                        self.memory.add_message(
                            "user",
                            "You did not use any tools. You MUST use the appropriate file tool "
                            "(`write_workspace_file`, `edit_workspace_file`, `run_terminal_command`, etc.) "
                            "to complete the task. Do not output raw code in chat. Try again."
                        )
                        current_loop += 1
                        continue
                    else:
                        return message.content or "Task completed."
                    
                # Execute tools safely
                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)
                    
                    # Log the tool call with relevant context
                    log_detail = func_args.get('filename', func_args.get('command', 'N/A'))
                    print(f"      [⚙️] AI is triggering tool: {func_name} | Target: {log_detail}")
                    
                    if func_name in self.tool_map:
                        try:
                            result = self.tool_map[func_name](**func_args)
                            print(f"      [✔] Tool Success: {result[:200]}") 
                            
                            # SELF-HEALING: If a run_terminal_command returns errors, 
                            # the result is fed back automatically via the tool message.
                            # The AI sees the error in context and can fix + retry.
                            
                        except Exception as e:
                            result = f"Error executing {func_name}: {str(e)}"
                            print(f"      [✖] Tool Failed: {result}")
                    else:
                        result = f"System Error: Tool '{func_name}' not found."
                    
                    self.memory.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": func_name,
                        "content": str(result)
                    })
                
            except Exception as e:
                error_string = str(e)
                print(f"      [!] API Error caught: {error_string}")
                
                self.memory.add_message(
                    "user",
                    f"Your last tool call failed with this API error: {error_string}. "
                    "Generate the tool call again using STRICT, valid JSON."
                )
            
            current_loop += 1
            
        return "Task aborted: Worker exceeded maximum tool execution loops."