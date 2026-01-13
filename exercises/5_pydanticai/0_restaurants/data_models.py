from pydantic import BaseModel, Field
from typing import Literal


class Restaurant(BaseModel):
    name: str = Field(description="Name of the restaurant")
    cuisine: str = Field(description="The type of food (cuisine) that the restaurant offers")
    price_level: Literal["Cheap", "Average", "Expensive"] = Field(description="The price level of the restaurant, Cheap, Average or Expensive")
    rating: int = Field(description="The restaurants rating from customers, between 1-5", gt=0, lt=6)
    opening_hours: str = Field(description="The hours the restaurant is open, example(08.00-16.00)")
    location: str = Field(description="The location of the restaurant")
    

class Prompt(BaseModel):
    prompt: str