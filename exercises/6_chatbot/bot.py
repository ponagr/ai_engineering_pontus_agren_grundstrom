from pydantic_ai import Agent 
from dotenv import load_dotenv
from pydantic_ai.agent import AgentRunResult
from pydantic import BaseModel
from pprint import pprint


load_dotenv()


class ChatBot:
    def __init__(self, system_prompt, questions):
        self.agent = Agent(
                model="google-gla:gemini-2.5-flash", 
                system_prompt=system_prompt, 
                output_type=AgentOutput
            )
        self.questions = questions
        self.result = None
        self.messages = []

    
    
    def chat(self, prompt: str) -> AgentRunResult:
        message_history = self.result.all_messages() if self.result else None
        self.result = self.agent.run_sync(prompt, message_history=message_history)
        
        self.questions = self.result.output.questions
        return {"user": prompt, "ai": self.result.output.result}
        

class AgentOutput(BaseModel):
    result: str
    questions: list[str]
    
    
    
if __name__ == "__main__":
    bot = ChatBot()
    result = bot.chat("Hej")
    result = bot.chat("hej2")
    
    pprint(result)
    pprint(bot.result.all_messages())