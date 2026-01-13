from pydantic_ai import Agent
from data_models import Restaurant
from dotenv import load_dotenv


load_dotenv()

food_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    system_prompt="Suggest a nearby restaurant based on the location and cuisine given in the prompt.",
    output_type=Restaurant
)



# exercise 0

# import asyncio

# food_agent = Agent(
#     model="google-gla:gemini-2.5-flash",
#     system_prompt="Suggest 5 nearby restaurants based on the location given in the prompt.",
#     output_type=list[Restaurant]
# )

# async def get_food(prompt):
#     result = await food_agent.run(prompt)
    
#     print(result)

# asyncio.run(get_food("Göteborg"))