import os
import json
from config import GROQ_API_KEY, DEFAULT_MODEL
from core.orchestrator import Orchestrator
from core.worker import WorkerAgent

def run_pipeline(user_goal: str):
    print(f"[!] Initializing Orchestrator...")
    orchestrator = Orchestrator(api_key=GROQ_API_KEY, model=DEFAULT_MODEL)
    
    print(f"[!] Generating structural execution plan...")
    tasks = orchestrator.plan(user_goal=user_goal)
    
    print(f"\n[+] Execution Roadmap Generated ({len(tasks)} steps):")
    for task in tasks:
        print(f" {task['id']}. [{task['title']}] - {task['description']}")
    print("-" * 60)
    
    worker = WorkerAgent(api_key=GROQ_API_KEY, model=DEFAULT_MODEL)
    
    for task in tasks:
        print(f"\n[*] Launching Task {task['id']}: {task['title']}")
        print(f"[*] Task Context: {task['description']}")
        
        result = worker.execute(task['description'])
        print(f"[+] Worker Response:\n{result}")
        
        print(f"[+] Task {task['id']} confirmed complete.")
        
if __name__ == "__main__":
    print("==================================================")
    print("  Orchestrator-Worker AI Framework Initialized    ")
    print("  Type 'exit' or press Ctrl+C to quit.            ")
    print("==================================================")
    
    while True:
        try:
            # 1. Capture the input directly from your terminal
            goal = input("\n[?] Enter your prompt: ")
            
            # 2. Handle empty inputs or exit commands cleanly
            if not goal.strip():
                continue
            if goal.lower() in ['exit', 'quit']:
                print("[!] Shutting down framework...")
                break
                
            # 3. Pass the dynamic input to the pipeline
            run_pipeline(goal)
            
        except KeyboardInterrupt:
            # Safely catch Ctrl+C so it doesn't throw an ugly traceback error
            print("\n[!] Force quitting...")
            break