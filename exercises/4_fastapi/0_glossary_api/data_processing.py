from pydantic import BaseModel, ValidationError
import json

def read_json(file_path):
with open("fastapi_glossary.json", "r") as f:
    data = f.read()
data = json.loads(data)

class Glossary(BaseModel):
    id: int
    word: str 
    meaning: str