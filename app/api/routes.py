from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from app.api.get_configs import get_settings_data
from app.chatbot.openai.controller import openai_chat
import os
import json

# Load the MODEL_DETAILS environment variable
try:
    model_details_json = os.getenv('MODEL_DETAILS')
    if model_details_json is None:
        raise ValueError("MODEL_DETAILS variable is not set")
    
    # Parse the JSON string
    model_details = json.loads(model_details_json)
except (ValueError, json.JSONDecodeError) as e:
    print(f"Error loading model details: {e}")
    model_details = []

# Create a dictionary to map model names to their details
model_details_dict = {model['model_name']: model for model in model_details}

# API Status
status_router = APIRouter()

@status_router.get("/")
def root():
    return RedirectResponse(url="/status")

@status_router.get("/status")
def check_api_status() -> dict[str, str]:
    return {"api_status":"Healthy"}

# Map the model names to the functions
model_methods = {}
for model in model_details:
    model_name = model['model_name']
    if model_name == "llama-31-8b-instruct":
        model_methods[model_name] = openai_chat
    elif model_name == "llama-31-70b-instruct":
        model_methods[model_name] = openai_chat
    elif model_name == "gpt-4o":
        model_methods[model_name] = openai_chat

chat_router = APIRouter()

@chat_router.post("/chat")
async def chat_endpoint(payload: dict):
    selected_model = payload.get("model")
    if not selected_model:
        raise ValueError("selected_model is missing or None")

    prompt = payload.get("prompt")
    if not prompt:
        raise ValueError("prompt is missing or None")

    temperature = payload.get("temperature")
    if temperature is None:
        raise ValueError("temperature is missing or None")

    max_tokens = payload.get("max_tokens")
    if max_tokens is None:
        raise ValueError("max_tokens is missing or None")

    vector_db = payload.get("vector_db")
    if not vector_db:
        raise ValueError("vector_db is missing or None")

    user = payload.get("user_id")
    if not user:
        raise ValueError("user ID is missing or None")

    # Get the function from the dictionary
    model_method = model_methods.get(selected_model)

    # If the model is not supported, return a 400 error
    if model_method is None:
        return {"answer": "The selected model is temporarily unavailable. Please try again later or choose a different option."}

    # Get the model details from the dictionary
    model_detail = model_details_dict.get(selected_model)
    if not model_detail:
        raise ValueError("Model details not found for the selected model")

    model_key = model_detail['model_key']
    model_url = model_detail['model_url']
    model_name = model_detail['model_name']

    # Call the model function with the parameters
    return model_method(prompt, temperature, max_tokens, vector_db, user, model_url, model_name, model_key)

# Settings
settings_router = APIRouter()

@settings_router.get("/settings")
def get_settings() -> dict:
    return get_settings_data()