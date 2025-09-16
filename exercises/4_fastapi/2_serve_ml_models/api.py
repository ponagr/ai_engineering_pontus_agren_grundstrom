from fastapi import FastAPI, Query, APIRouter
from pydantic import BaseModel, Field
import pandas as pd
import joblib
from constants import DATA_PATH, MODEL_PATH

# e) Read this model and create an API around it. 
# You should have endpoints to be able to read the data, do some filterings and be able to send in data to get prediction back.

df = pd.read_csv(DATA_PATH / "auto-mpg.csv").rename(columns={"model year": "model_year"})

router = APIRouter(prefix="/api/mpg")

app = FastAPI()


class MpgInput(BaseModel):
    cylinders: int = Field(gt=1, lt=9)
    displacement: float = Field(gt=65, lt=460)
    horsepower: int = Field(gt=40, lt=240)
    weight: int = Field(gt=1600, lt=5200)
    acceleration: float = Field(gt=5, lt=26)
    model_year: int = Field(gt=65, lt=85)

class PredictionResponse(BaseModel):
    predicted_mpg: float


@router.get("")
def read_data(limit: int = 392):
    return df.head(limit).to_dict(orient="records")


@router.get("/", description="Filter by more than input.")
def filter_data(cylinders: int = Query(None, gt=1, lt=9),
                displacement: float = Query(None, gt=65, lt=460),
                horsepower: int = Query(None, gt=40, lt=240),
                weight: int = Query(None, gt=1600, lt=5200),
                acceleration: float = Query(None, gt=5, lt=26),
                model_year: int = Query(None, gt=65, lt=85),
                mpg: float = Query(None, gt=8, lt=50)
            ):
    
    filtered_df = df
    
    if cylinders:
        filtered_df = filtered_df.query("cylinders >= @cylinders")
    if displacement:
        filtered_df = filtered_df.query("displacement >= @displacement")
    if horsepower:
        filtered_df = filtered_df.query("horsepower >= @horsepower")
    if weight:
        filtered_df = filtered_df.query("weight >= @weight")
    if acceleration:
        filtered_df = filtered_df.query("acceleration >= @acceleration")
    if model_year:
        filtered_df = filtered_df.query("model_year >= @model_year")
    if mpg:
        filtered_df = filtered_df.query("mpg >= @mpg")    
    
    return filtered_df.to_dict(orient="records")


@router.post("/predict", response_model=PredictionResponse)
def predict_mpg(payload: MpgInput):
    predict_data = pd.DataFrame([payload.model_dump()])
    model = joblib.load(MODEL_PATH / "mpg_regressor.joblib")
    prediction = model.predict(predict_data)
    
    return {"predicted_mpg": prediction[0]}

  
app.include_router(router)