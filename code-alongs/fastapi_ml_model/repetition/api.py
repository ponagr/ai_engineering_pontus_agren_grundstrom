from fastapi import FastAPI
from data_processing import IrisData, IrisInput, IrisPredictionOutput
import joblib
from constants import MODELS_PATH
import pandas as pd


app = FastAPI()


@app.get("/iris/")
async def read_data():
    iris = IrisData()
    return iris.to_json()


@app.post("/iris/predict/", response_model=IrisPredictionOutput)
async def predict_flower(payload: IrisInput):
    data_to_predict = pd.DataFrame([payload.model_dump()])
    clf = joblib.load(MODELS_PATH / "iris_classifier.joblib")
    
    prediction = clf.predict(data_to_predict)
    
    return {"predicted_flower": prediction[0]}
    