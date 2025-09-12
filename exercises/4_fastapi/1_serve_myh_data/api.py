from fastapi import FastAPI, Query, APIRouter
from contextlib import asynccontextmanager
import pandas as pd
from constants import DATA_PATH
from data_processing import DataExplorer


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.df = pd.read_excel(DATA_PATH / "resultat-ansokningsomgang-2024.xlsx", sheet_name="Tabell 3", header=5)
    yield 
    del app.state.df

# tabell_3 = tabell_data()

app = FastAPI(lifespan=lifespan)


@app.get("/tabell3")
async def filter_tabell3(
    school: str = Query(None, description="Filter data by school name"),
    field: str = Query(None, description="Filter data by school field")
):
    data = DataExplorer(app.state.df)

    return data.filter(school, field)


# @app.get("/tabell3/summary")
# async def read_summary():
#     data = DataExplorer(app.state.df)
    
#     return data.summary()


@app.get("/tabell3/kpis")
async def read_kpis(column: str = Query(None, description="get kpi for a specific column, or get a summary description of df")):
    data = DataExplorer(app.state.df)
    
    return data.kpis(column)


    
    

# b) Make an API endpoint where you serve table 3 in JSON format for a read operation.
# @app.get("/tabell3")
# async def read_tabell3():
#     data = DataExplorer(app.state.df)
    
#     return data.json_response()


# c) Make endpoints where you could filter out a particular school.
# @app.get("/tabell3/school")
# async def filter_school(school: str): # = Query(None, description="Filter tabell 3 by school name")):
#     if school:
#         return [data for data in tabell_3 if school.casefold() in data.get("Utbildningsanordnare administrativ enhet").casefold()]


# d) Make endpoints where you could filter out a particular field.
# @app.get("/tabell3/field")
# async def filter_field(field: str):
#     if field:
#         return [data for data in tabell_3 if field.casefold() in data.get("Utbildningsområde").casefold()]


# e) Make endpoint for approved (beviljad) and one for not approved (avslag).
# @app.get("/tabell3/approved")
# async def approved_schools():
#     return [data for data in tabell_3 if data.get("Beviljade platser totalt") > 0]


# @app.get("/tabell3/rejected")
# async def rejected_schools():
#     return [data for data in tabell_3 if data.get("Beviljade platser totalt") == 0]


# @app.get("/tabell3/beslut/")
# async def rejected_schools(beslut: str = Query(None)):
#     return [data for data in tabell_3 if beslut.casefold() in data.get("Beslut").casefold()]


# f) Make an endpoint for some KPIs that you think is interesting for a particular stakeholder in mind.
# @app.get("/tabell3/kpis")
# mest avslagna/beviljade ansökningar, baserat på:
    # län, kommun, utbildningsområde, sun5 inriktnings namn, huvudmannatyp, studietakt, studieform, flera kommuner, smalt yrkesområde, yh poäng
# för varje skola, % på hur många beviljade, baserat på sökta utbildningsomgångar.sum()/beviljade utbildningsomgångar, och sökta/beviljade platser totalt


# g) What else do you want to be able to serve?
# inriktning(sun5 inrikning namn)
# alla skolor inom en kommun/län
# studieform
# studietakt