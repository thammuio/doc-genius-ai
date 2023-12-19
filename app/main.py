"""Main entrypoint for the app."""
import threading
import uvicorn

from app.api.routes import chat_router, status_router, settings_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

def create_app():
    CDSW_DOMAIN = os.getenv('CDSW_DOMAIN')
    CDSW_APP_PORT = os.getenv('CDSW_APP_PORT')
    app = FastAPI()
    app.add_middleware(
    CORSMiddleware,
    allow_origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://{}:{}".format(CDSW_DOMAIN, CDSW_APP_PORT),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    )
    app.include_router(status_router)
    app.include_router(chat_router)
    app.include_router(settings_router)
    return app

def run_server(app, host="0.0.0.0", port=None, log_level="warning", reload=False):
    if port is None:
        port = int(os.getenv('CDSW_APP_PORT', 8080))  # Default to 8080 if API_PORT is not set
    uvicorn.run(app, host=host, port=port, log_level=log_level, reload=reload)

def main():
    app = create_app()
    server_thread = threading.Thread(target=run_server, args=(app,))
    server_thread.start()

if __name__ == "__main__":
    main()