from pydantic_ai import Agent 
from dotenv import load_dotenv
from pydantic_ai.agent import AgentRunResult
from pydantic import BaseModel
from pprint import pprint


load_dotenv()


class StoryTeller:
    def __init__(self):
        self.agent = Agent(
                model="google-gla:gemini-2.5-flash", 
                system_prompt="Generera korta berättelser för barn, samt 3 frågor relaterade till ämnet", 
                output_type=AgentOutput
            )
        self.questions = ["Skriv en historia om en kanin", "Skriv en historia om en apa", "Skriv en historia om en drake"]
        self.result = None
    
    
    def chat(self, prompt: str) -> AgentRunResult:
        message_history = self.result.all_messages() if self.result else None
        self.result = self.agent.run_sync(prompt, message_history=message_history)
        
        self.questions = self.result.output.questions
        
        return {"user": prompt, "ai": self.result.output.result}
        

class AgentOutput(BaseModel):
    result: str
    questions: list[str]
    
    
    
if __name__ == "__main__":
    bot = StoryTeller()
    result = bot.chat("Hej")
    result = bot.chat("hej2")
    
    pprint(result)
    pprint(bot.result.all_messages())