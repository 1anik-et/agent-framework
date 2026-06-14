import sys
from core.worker import WorkerAgent

def main():
    agent = WorkerAgent(system_prompt="You are an autonomous engineering system. Use your workspace tools to complete tasks directly.")
    print("Level 2 ReAct Engine Initialized, (Groq Llama-3 engine). Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            if not user_input.strip():
                continue
            
            print("\n---Framework Exectution Trace---")
            for chunk in agent.execute_task(user_input):
                sys.stdout.write(chunk)
                sys.stdout.flush()
            print("\n" + "-"*100)            
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nSystem Error: {str(e)}\n")
            
if __name__ == "__main__":
    main()