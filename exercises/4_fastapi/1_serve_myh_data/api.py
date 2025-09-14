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


app = FastAPI(lifespan=lifespan)

tabell3_router = APIRouter(prefix="/api/tabell3")

# b) Make an API endpoint where you serve table 3 in JSON format for a read operation.
# c) Make endpoints where you could filter out a particular school.
# d) Make endpoints where you could filter out a particular field.
@tabell3_router.get("")
async def filter_tabell3(school: str = Query(None, description="Filter data by school name"),
                         field: str = Query(None, description="Filter data by school field")):
    
    data = DataExplorer(app.state.df)

    return data.filter(school, field)

#e) Make endpoint for approved (beviljad) and one for not approved (avslag).
@tabell3_router.get("/approved")
async def approved_schools():
    data = DataExplorer(app.state.df)
    
    return data.decision(True)

#e) Make endpoint for approved (beviljad) and one for not approved (avslag).
@tabell3_router.get("/rejected")
async def rejected_schools():
    data = DataExplorer(app.state.df)
    
    return data.decision(False)


@tabell3_router.get("/summary")
async def read_summary():
    data = DataExplorer(app.state.df)
    
    return data.summary()



# f) Make an endpoint for some KPIs that you think is interesting for a particular stakeholder in mind.
@tabell3_router.get("/kpis")
async def read_kpis(column: str = Query(None, description="get kpi for total applications and total approved spots for each unique value within a specific column")):
    data = DataExplorer(app.state.df)
    
    return data.kpis(column)


app.include_router(tabell3_router)    


# g) What else do you want to be able to serve?

# inriktning(sun5 inrikning namn)
# alla skolor inom en kommun/län
# studieform
# studietakt