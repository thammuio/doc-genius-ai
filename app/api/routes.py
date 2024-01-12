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
    prompt = payload.get("prompt")
    parameters = payload.get("parameters")
    temperature = parameters.get("temperature")
    max_tokens = parameters.get("max_tokens")
    selected_vector_db = payload.get("selected_vector_db")
    user = payload.get("user")

    # Get the function from the dictionary
    model_method = model_methods.get(selected_model)

    # If the model is not supported, return a 400 error
    if model_method is None:
        raise HTTPException(status_code=400, detail="Model not supported / Work in Progress")

    # Call the model function with the parameters
    return model_method(prompt, temperature, max_tokens, selected_vector_db, user)


# Settings
settings_router = APIRouter()

@settings_router.get("/settings")
def get_settings() -> dict:
    return get_settings_data()
