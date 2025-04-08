from dishka import Provider, provide, Scope

from elasticsearch import Elasticsearch

from src.settings import settings


class LangchainProvider(Provider):
    @provide(scope=Scope.APP)
    def get_elasticsearch(self) -> Elasticsearch:
        return Elasticsearch(
            hosts=settings.elasticsearch.url,
            basic_auth=(settings.elasticsearch.user, settings.elasticsearch.password),
            verify_certs=False
        )
