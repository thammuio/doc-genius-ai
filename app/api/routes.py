from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.utils.sanity import status_gpu_check
from app.chatbot.model import TextInput, generate_text
from app.api.get_configs import get_settings_data


# API Status
status_router = APIRouter()

@status_router.get("/")
def root():
    return RedirectResponse(url="/status")

@status_router.get("/status")
def check_gpu_status() -> dict[str, str]:
    return status_gpu_check()

# Chat
chat_router = APIRouter()

@chat_router.post("/chat")
def post_generate_text(data: TextInput) -> dict[str, str]:
    return generate_text(data)


# Settings
settings_router = APIRouter()

@settings_router.get("/settings")
def get_settings() -> dict:
    return get_settings_data()
