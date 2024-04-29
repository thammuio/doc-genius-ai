from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from app.api.get_configs import get_settings_data
from app.chatbot.llama2_7B_chat.controller import llama_2_7b_chat
from app.chatbot.llama2_13B_chat.controller import llama_2_13b_chat
from app.chatbot.llama3_8B_instruct.controller import llama_3_8b_instruct
from app.chatbot.zephyr_7B_alpha.controller import zephyr_7B_alpha
from app.chatbot.llama2_7B_chat_hf.controller import llama2_7b_chat_hf
from app.chatbot.mistral_7B_instruct.controller import mistral_7b_instruct

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
    "llama-2-7B-chat": llama_2_7b_chat,
    "llama-2-13B-chat": llama_2_13b_chat,
    "Meta-Llama-3-8B-Instruct": llama_3_8b_instruct,
    "zephyr-7B-alpha": zephyr_7B_alpha,
    "Llama-2-7b-chat-hf": llama2_7b_chat_hf,
    "Mistral-7B-Instruct": mistral_7b_instruct
}

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
        raise ValueError("selected_vector_db is missing or None")

    user = payload.get("user_id")
    if not user:
        raise ValueError("user ID is missing or None")

    # Get the function from the dictionary
    model_method = model_methods.get(selected_model)

    # If the model is not supported, return a 400 error
    if model_method is None:
        return {"answer": "Selected Model is currently not Available"}

    # Call the model function with the parameters
    return model_method(prompt, temperature, max_tokens, vector_db, user)


# Settings
settings_router = APIRouter()

@settings_router.get("/settings")
def get_settings() -> dict:
    return get_settings_data()
