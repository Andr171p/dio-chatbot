import logging
from pathlib import Path

from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.retrievers import ElasticSearchBM25Retriever


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH = BASE_DIR / "raw" / "price_1c.xls"

loader = UnstructuredExcelLoader(FILE_PATH)

documents = loader.load()

text = documents[0].page_content

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=20,
    length_function=len,
)

chunks = text_splitter.create_documents([text])
log.info("Всего чанков %s", len(chunks))

embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    model_kwargs={"device": "cpu"},
    encode_kwargs={'normalize_embeddings': False},
)
log.info("Модель ембеддингов загружена")

elastic_client = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", "password"),
    verify_certs=False
)

indices = elastic_client.cat.indices(h='index').split()

for index in indices:
    try:
        elastic_client.indices.delete(index=index, ignore=[400, 404])
        print(f"Удалён индекс {index}")
    except Exception as e:
        print(f"Произошла ошибка при удалении индекса {index}: {e}")

elastic_store = ElasticsearchStore(
    es_connection=elastic_client,
    index_name="dio-vector-index",
    embedding=embeddings,
    es_user="elastic",
    es_password="password"
)

bm25_retriever = ElasticSearchBM25Retriever(
    client=elastic_client,
    index_name="dio-docs-index",
)

'''elastic_store.add_documents(documents=chunks)
log.info("Документы добавлены в векторное хранилище")

bm25_retriever.add_texts([document.page_content for document in chunks])
log.info("Документы добавлены в индекс BM25")'''
