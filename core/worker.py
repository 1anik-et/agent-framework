import json
import time
from groq import Groq
from config import GROQ_API_KEY, DEFAULT_MODEL
from core.memory import MemoryManager
from tools.registry import GROQ_TOOLS, TOOL_MAP

class WorkerAgent:
    def __init__(self, system_prompt: str = "You are an expert programming assistant."):
        # Initializing the native Groq client
        self.client = Groq(api_key=GROQ_API_KEY)
        self.memory = MemoryManager(system_prompt)
        self.model = DEFAULT_MODEL

    def execute_task(self, user_input: str):
        """Runs an autonomous ReAct loop allowing the model to use tools iteratively."""
        self.memory.add_message("user", user_input)
        
        max_loops = 5  # Prevent accidental infinite execution loops
        
        for loop_idx in range(max_loops):
            try:
                # Pass both messages AND the tools schema array to Groq
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.memory.get_context(),
                    tools=GROQ_TOOLS,
                    tool_choice="auto"
                )
                
                message = response.choices[0].message
                tool_calls = message.tool_calls
                
                # Case A: Model wants to speak directly to the user (No tools called)
                if not tool_calls:
                    if message.content:
                        self.memory.add_message("assistant", message.content)
                        yield message.content
                    return
                
                # Case B: Model calls one or more tools
                # First, append the assistant's tool-intent message to maintain correct history order
                self.memory.messages.append(message)
                
                for tool_call in tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)
                    
                    yield f"\n[Action] Invoking tool '{func_name}' with args: {func_args}\n"
                    
                    # Execute the local python fucntion safely
                    if func_name in TOOL_MAP:
                        tool_output = TOOL_MAP[func_name](**func_args)
                    else:
                        tool_output = f"Error: Tool '{func_name}' is not registered."
                    
                    yield f"[Observation] Result: {tool_output}\n"
                    
                    # Append the tool's performance output back to the model's history window   
                    self.memory.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": func_name,
                        "content": tool_output
                    })
                    
                # Continue the loop automatically so the model analyzes its tool outputs
                yield "\n[Thinking] Analyzing execution results...\n"
            except Exception as e:
                yield f"\n[Execution Exception Error]: {str(e)}"
                return