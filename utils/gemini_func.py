from google import genai
from dotenv import load_dotenv
import os
from pydantic import BaseModel

# class ClassName(BaseModel):
#     name: str 

# lägg till: 
# config={
#         "response_mime_type": "application/json",
#         "response_schema": list[ClassName],
#     },
# response = client.models.generate_content(model=model, contents=prompt, config={
#         "response_mime_type": "application/json",
#         "response_schema": list[ClassName],
#     },)

# output från response
# my_recipes: list[ClassName] = response.parsed

def fix_prompt(data = None, output_examples = None, rules: str = None, task: str = None, role: str = None, output_format: str = None) -> str:
    parts = []
    
    if role:
        parts.append(f"Du är {role}.")
    if task:
        parts.append(f"Din uppgift är: {task}")
    if rules:
        parts.append(f"Följ dessa regler:\n{rules}")
    if data:
        parts.append(f"Här är data du ska arbeta med:\n{data}")
    if output_examples:
        parts.append(f"Exempel på önskat output:\n{output_examples}")
    if output_format:
        parts.append(f"Format på svaret:\n{output_format}")
    prompt = "\n\n".join(parts)
    
    return prompt


def ask_gemini(prompt: str, model="gemini-2.5-flash", config=None) -> str:
    """
    Tips: Anropa fix_prompt() istället för en prompt direkt som argument för att bygga ihop en prompt direkt i anropet
    """
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    
    if not prompt:
        prompt = "Hej Gemini! Detta är ett test för att se om funktionen fungerar. Svara kort: fungerar du?"
    
    response = client.models.generate_content(model=model, contents=prompt, config=config)
    
    return response.text