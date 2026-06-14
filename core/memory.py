class MemoryManager:
    def __init__(self, system_prompt: str):
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
        
    def add_message(self, role: str, content: str):
        # Role must be either 'user' or 'model'
        self.messages.append({"role": role, "content": content})
        
    def get_context(self):
        return self.messages
    
    def clear(self):
        # Keep the system prompt if memory is closed
        system = self.messages[0] if self.messages and self.messages[0]["role"] == "system" else None
        self.messages = [system] if system else []  