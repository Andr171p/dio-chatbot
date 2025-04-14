from dishka import Provider, provide, Scope

from src.services.connection_managers import (
    BaseConnectionManager,
    InMemoryConnectionManager
)


class ServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_connection_manager(self) -> BaseConnectionManager:
        return InMemoryConnectionManager()
