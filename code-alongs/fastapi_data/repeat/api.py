from fastapi import FastAPI, APIRouter
from data_processing import DataExplorer


app = FastAPI()
sales_router = APIRouter(prefix="/api/sales")


@sales_router.get("")
async def read_sales():
    return DataExplorer().json_response()


@sales_router.get("/summary")
async def read_summary_data():
    return DataExplorer().summary().json_response()


@sales_router.get("/kpis")
async def read_kpis_by_country(country: str):
    return DataExplorer().kpis(country)


app.include_router(sales_router)