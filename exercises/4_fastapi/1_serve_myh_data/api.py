from fastapi import FastAPI, Query
from data_processing import read_excel


data = read_excel()

app = FastAPI()


@app.get("/tabell3")
def read_tabell3():
    return data