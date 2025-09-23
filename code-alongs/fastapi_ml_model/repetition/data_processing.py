from constants import DATA_PATH
import pandas as pd
from pydantic import BaseModel, Field
from typing import Literal
from pprint import pprint


df = pd.read_csv(DATA_PATH / "IRIS.csv")


class IrisData():
    def __init__(self):
        self.df = df
    
    def to_json(self):
        return self.df.to_dict(orient="records")


class IrisInput(BaseModel):
    sepal_length: float = Field(gt=4, lt=8.1) 
    sepal_width: float = Field(gt=1.8, lt=4.7) 
    petal_length: float = Field(gt=0.8, lt=7.1) 
    petal_width: float = Field(gt=0, lt=2.7) 

class IrisPredictionOutput(BaseModel):
    predicted_flower: str = Literal["Iris-setosa", "Iris-versicolor", "Iris-virginica"] # why u no work???


if __name__ == "__main__":
    iris = IrisData()
    pprint(iris.to_json())