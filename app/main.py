"""Main entrypoint for the app."""
import threading
import uvicorn

from app.api.routes import chat_router, status_router, settings_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

def create_app():
    CDSW_DOMAIN = os.getenv('CDSW_DOMAIN')
    app = FastAPI()
    app.add_middleware(
    CORSMiddleware,
    allow_origins = [
    "*",
    f"https://docgenius-api.{CDSW_DOMAIN}",
    f"https://docgenius-ui.{CDSW_DOMAIN}",
    f"https://{CDSW_DOMAIN}",
    f"https://*.{CDSW_DOMAIN}",
    f"*.{CDSW_DOMAIN}",
    "*.cloudera.site",
    "http://localhost:3000",
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

def run_server(app, host="127.0.0.1", port=None, log_level="warning", reload=False):
    if port is None:
        port = int(os.getenv('CDSW_APP_PORT', 9000))  # Default to 8080 if API_PORT is not set
    uvicorn.run(app, host=host, port=port, log_level=log_level, reload=reload)

def main():
    app = create_app()
    server_thread = threading.Thread(target=run_server, args=(app,))
    server_thread.start()

if __name__ == "__main__":
    main()
