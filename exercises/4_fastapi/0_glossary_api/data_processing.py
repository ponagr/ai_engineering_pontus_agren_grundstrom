from pydantic import BaseModel, Field, ValidationError
import json
from constants import DATA_PATH
from pprint import pprint


# Read the data from this repository called `fastapi_glossary.json`. Create Pydantic model(s) of the data in a separate script called `data_processing.py`.

def read_json(file_name):
    with open(DATA_PATH/file_name, "r") as file:
        return json.load(file)
        

class Glossary(BaseModel):
    id: int = Field(gt=-1)
    word: str 
    meaning: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 15,
                "word": "serialization",
                "meaning": "Converting a python-object(dict, list) into a json-object(string)."
            }
        }
    }


def glossary_data(filename):
    json_data = read_json(filename)
    return [Glossary.model_validate(item) for item in json_data]


if __name__ == "__main__":
    try:
        glossary = glossary_data("fastapi_glossary.json")
        pprint(glossary)
    except ValidationError as err:
        pprint(err)