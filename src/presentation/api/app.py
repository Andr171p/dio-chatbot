from litestar import Litestar
from dishka.integrations.litestar import setup_dishka

from src.presentation.api.v1.routers import ChatWebsocketListener
from src.di.container import container


def get_litestar_app() -> Litestar:
    app = Litestar(route_handlers=[ChatWebsocketListener])
    setup_dishka(app=app, container=container)
    return app
