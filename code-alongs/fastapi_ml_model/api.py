from fastapi import FastAPI, APIRouter
import pandas as pd
import joblib
from constants import DATA_PATH, MODELS_PATH
from pydantic import BaseModel, Field


df = pd.read_csv(DATA_PATH / "IRIS.csv")

router = APIRouter(prefix="/api/iris/v1")

app = FastAPI()


# request/response schemas
class IrisInput(BaseModel):
    sepal_length: float = Field(lt=8.5, gt=4)
    sepal_width: float = Field(lt=5, gt=1.8)
    petal_length: float = Field(lt=7.5, gt=0.8)
    petal_width: float = Field(lt=3, gt=0)

class PredictionOutput(BaseModel):
    predicted_flower: str


@router.get("")
def read_data():
    return df.to_dict(orient="records")

@router.post("/predict", response_model=PredictionOutput)
def predict_flower(payload: IrisInput):
    data_to_predict = pd.DataFrame([payload.model_dump()])
    clf = joblib.load(MODELS_PATH / "iris_classifier.joblib")
    prediction = clf.predict(data_to_predict)
    
    return {"predicted_flower": prediction[0]}



app.include_router(router=router)
