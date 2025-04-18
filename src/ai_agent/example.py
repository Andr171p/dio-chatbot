import logging
import asyncio

from elasticsearch import Elasticsearch
from langchain.retrievers import EnsembleRetriever
from langchain_elasticsearch import ElasticsearchStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import ElasticSearchBM25Retriever

from src.ai_agent.react_agent import ReACTAgent

from src.llms.yandex_gpt import YandexGPTChatModel
from src.ai_agent.tools import RetrievalTool, SearchProductTool
from src.misc.files import read_txt
from src.settings import settings, BASE_DIR


embeddings = HuggingFaceEmbeddings(
    model_name=settings.embeddings.model_name,
    model_kwargs=settings.embeddings.model_kwargs,
    encode_kwargs=settings.embeddings.encode_kwargs
)


elasticsearch_client = Elasticsearch(
    hosts=settings.elasticsearch.url,
    basic_auth=(settings.elasticsearch.user, settings.elasticsearch.password),
    verify_certs=False
)


vector_store = ElasticsearchStore(
    es_connection=elasticsearch_client,
    index_name="dio-vector-index",
    embedding=embeddings,
    es_user=settings.elasticsearch.user,
    es_password=settings.elasticsearch.password
)

bm25_retriever = ElasticSearchBM25Retriever(
    client=elasticsearch_client,
    index_name="dio-docs-index"
)

vector_store_retriever = vector_store.as_retriever()

retriever = EnsembleRetriever(
    retrievers=[vector_store_retriever, bm25_retriever],
    weights=[0.6, 0.4]
)

model = YandexGPTChatModel(
    api_key=settings.yandex_gpt.api_key,
    folder_id=settings.yandex_gpt.folder_id,
    model="yandexgpt"
)


async def main() -> None:
    file_path = BASE_DIR / "data" / "processed" / "price_list.csv"
    db_url = settings.sqlite.db_path
    print(db_url)
    retrieval_tool = RetrievalTool(retriever)
    search_product_tool = SearchProductTool(file_path)
    prompt_template = read_txt(settings.prompts.system_path)
    agent = ReACTAgent(
        db_url=db_url,
        tools=[retrieval_tool, search_product_tool],
        prompt_template=prompt_template,
        model=model
    )
    thread_id = "2"
    while True:
        query = input("User: ")
        if query == "q":
            break
        message = await agent.generate(thread_id, query)
        print(message)
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
