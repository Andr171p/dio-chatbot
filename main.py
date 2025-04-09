import logging

from src.presentation.api.app import get_fastapi_app


logging.basicConfig(level=logging.INFO)

app = get_fastapi_app()
