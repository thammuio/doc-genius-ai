from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from app.api.get_configs import get_settings_data
from app.chatbot.poc.controller import poc_gpu_rag_llama_2_13b_chat

# API Status
status_router = APIRouter()

@status_router.get("/")
def root():
    return RedirectResponse(url="/status")

@status_router.get("/status")
def check_api_status() -> dict[str, str]:
    return {"api_status":"Healthy"}

# Chat
# Map the model names to the functions
model_methods = {
    "poc/gpu/rag/llama-2-13b-chat": poc_gpu_rag_llama_2_13b_chat
    # Add more models here
}

chat_router = APIRouter()

@chat_router.post("/chat")
async def chat_endpoint(payload: dict):
    selected_model = payload.get("selected_model")
    if not selected_model:
        raise ValueError("selected_model is missing or None")

    prompt = payload.get("prompt")
    if not prompt:
        raise ValueError("prompt is missing or None")

    parameters = payload.get("parameters", {"temperature": 1,"max_tokens": 100})
    if not parameters:
        raise ValueError("parameters is missing or None")

    temperature = parameters.get("temperature")
    if temperature is None:
        raise ValueError("temperature is missing or None")

    max_tokens = parameters.get("max_tokens")
    if max_tokens is None:
        raise ValueError("max_tokens is missing or None")

    selected_vector_db = payload.get("selected_vector_db", "MILUS")
    if not selected_vector_db:
        raise ValueError("selected_vector_db is missing or None")

    user = payload.get("user", "genius")
    if not user:
        raise ValueError("user is missing or None")

    # Get the function from the dictionary
    model_method = model_methods.get(selected_model)

    # If the model is not supported, return a 400 error
    if model_method is None:
        return {"answer": "Selected Model not supported yet / Work in Progress"}

    # Call the model function with the parameters
    return model_method(prompt, temperature, max_tokens, selected_vector_db, user)


# Settings
settings_router = APIRouter()

@settings_router.get("/settings")
def get_settings() -> dict:
    return get_settings_data()
