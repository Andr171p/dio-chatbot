from dishka import Provider, provide, Scope

from elasticsearch import Elasticsearch
from langchain_core.embeddings import Embeddings
from langchain.retrievers import EnsembleRetriever
from langchain_community.llms.yandex import YandexGPT
from langchain_elasticsearch import ElasticsearchStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.language_models import BaseChatModel, BaseLLM
from langchain_community.retrievers import ElasticSearchBM25Retriever

from src.settings import settings


class LangchainProvider(Provider):
    @provide(scope=Scope.APP)
    def get_embeddings(self) -> Embeddings:
        return HuggingFaceEmbeddings(
            model_name=settings.embeddings.model_name,
            model_kwargs=settings.embeddings.model_kwargs,
            encode_kwargs=settings.embeddings.encode_kwargs
        )

    @provide(scope=Scope.APP)
    def get_elasticsearch(self) -> Elasticsearch:
        return Elasticsearch(
            hosts=settings.elasticsearch.url,
            basic_auth=(settings.elasticsearch.user, settings.elasticsearch.password),
            verify_certs=False
        )

    @provide(scope=Scope.APP)
    def get_elasticsearch_store(
            self,
            elasticsearch: Elasticsearch,
            embeddings: Embeddings
    ) -> ElasticsearchStore:
        return ElasticsearchStore(
            es_connection=elasticsearch,
            index_name="dio-vector-index",
            embedding=embeddings,
            es_user=settings.elasticsearch.user,
            es_password=settings.elasticsearch.password
        )

    @provide(scope=Scope.APP)
    def get_bm25_retriever(self, elasticsearch: Elasticsearch) -> ElasticSearchBM25Retriever:
        return ElasticSearchBM25Retriever(
            client=elasticsearch,
            index_name="dio-docs-index"
        )

    @provide(scope=Scope.APP)
    def get_vector_store_retriever(self, vector_store: ElasticsearchStore) -> VectorStoreRetriever:
        return vector_store.as_retriever()

    @provide(scope=Scope.APP)
    def get_retriever(
            self,
            vector_store_retriever: VectorStoreRetriever,
            bm25_retriever: ElasticSearchBM25Retriever
    ) -> EnsembleRetriever:
        return EnsembleRetriever(
            retrievers=[vector_store_retriever, bm25_retriever],
            weights=[0.6, 0.4]
        )

    @provide(scope=Scope.APP)
    def get_model(self) -> BaseChatModel | BaseLLM:
        return YandexGPT(
            api_key=settings.yandex_gpt.api_key,
            folder_id=settings.yandex_gpt.folder_id
        )
