from fastapi import FastAPI
from data_models import Prompt, Restaurant
from agent import food_agent
from utils import query_duckdb


app = FastAPI()


@app.get("/restaurants")
async def get_restaurants():
    restaurants = query_duckdb("FROM restaurants;")
    
    return restaurants.to_dict(orient="records")


@app.post("/find_restaurants")
async def find_restaurants(prompt: Prompt):
    result = await food_agent.run(prompt.prompt)
    restaurant = result.output
    
    
    query_duckdb(
        "INSERT INTO restaurants VALUES (?,?,?,?,?,?)",
        parameters=[
            restaurant.name, 
            restaurant.cuisine, 
            restaurant.price_level, 
            restaurant.rating, 
            restaurant.opening_hours, 
            restaurant.location
        ]
    )
    
    return restaurant
    
    
