from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka

from src.di.container import container
from src.presentation.api.v1.routers import (
    chat_router,
    chat_socket_router
)


def get_fastapi_app() -> FastAPI:
    app = FastAPI()
    app.include_router(chat_router)
    app.include_router(chat_socket_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_dishka(
        container=container,
        app=app
    )
    return app
