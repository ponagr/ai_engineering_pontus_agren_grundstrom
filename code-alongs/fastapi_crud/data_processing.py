import json
from constants import DATA_PATH, CURRENT_YEAR
from pprint import pprint
from pydantic import BaseModel, Field

def read_json(file_name):
    with open(DATA_PATH / file_name, "r") as file:
        return json.load(file)

class Book(BaseModel):
    id: int
    title: str 
    author: str
    year: int = Field(gt=1000, lt=CURRENT_YEAR+1)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 11,
                "title": "harry ponta",
                "author": "ponne&naz",
                "year": 1007
            }
        }
    }

class Library(BaseModel):
    name: str 
    books: list[Book]

def library_data(filename):
    json_data = read_json(filename)
    return Library.model_validate(json_data)

if __name__ == "__main__":
    library = library_data("library.json")
    pprint(library)

    