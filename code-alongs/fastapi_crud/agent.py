from pydantic_ai import Agent 
from data_processing import Book
from dotenv import load_dotenv

load_dotenv()

book_agent = Agent(model="google-gla:gemini-2.5-flash", system_prompt="Generate a book based on the prompt", output_type=Book)