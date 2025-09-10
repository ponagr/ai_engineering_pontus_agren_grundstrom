from fastapi import FastAPI, Query
from data_processing import glossary_data, Glossary
from pprint import pprint
from pydantic import ValidationError



try:
    glossarys = glossary_data("fastapi_glossary.json")
    # glossary = [{"word":glos.word, "meaning":glos.meaning} for glos in glossary_list]
    pprint(glossarys)
except ValidationError as err:
    pprint(err)


app = FastAPI()

# a) Now create an endpoint `/glossary` which will return all words and their meaning.
@app.get("/glossary")
async def read_glossary():
    return [glos for glos in glossarys]


# b) Create a query parameter to filter out a specific word
@app.get("/glossary/")
async def filter_glossary(word: str = Query(None, description="Filter by word in glossary")):
    if word:
        return [glos for glos in glossarys if glos.word.casefold() in word.casefold()]


# c) Turn your API into a CRUD API, so that you can add glossary, update and delete glossary.
@app.post("/glossary/add_glossary")
async def add_glossary(glossary_request: Glossary):
    new_glossary = Glossary.model_validate(glossary_request)
    glossarys.append(new_glossary)
    
    return new_glossary


@app.put("/glossary/update_glossary")
async def update_glossary(updated_glossary: Glossary):
    for i, glos in enumerate(glossarys):
        if glos.id == updated_glossary.id:
            glossarys[i] = updated_glossary
    
    return updated_glossary


@app.delete("/glossary/delete_glossary/{id}")
async def delete_glossary(id: int):
    for i, glos in enumerate(glossarys):
        if id == glos.id:
            deleted = glossarys[i]
            del glossarys[i]
            return f"Deleted: {deleted}", f"Updated glossary: {glossarys}"
            # break