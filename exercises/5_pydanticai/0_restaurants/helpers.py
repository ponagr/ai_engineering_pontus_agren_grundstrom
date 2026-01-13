import requests

URL = "http://127.0.0.1:8000"

def ask_chatbot(text):
    stuff = {
        "prompt": text
    }
    
    response = requests.post(f"{URL}/find_restaurants", json=stuff)
    
    return response.text

def show_all():
    response = requests.get(f"{URL}/restaurants")
    
    return response.json()
