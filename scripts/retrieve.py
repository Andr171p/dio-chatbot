from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.retrievers import ElasticSearchBM25Retriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.retrievers import EnsembleRetriever


embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    model_kwargs={"device": "cpu"},
    encode_kwargs={'normalize_embeddings': False},
)

elastic_client = Elasticsearch(
    hosts="https://localhost:9200",
    basic_auth=("elastic", "password"),
    verify_certs=False
)

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

vector_store_retriever = elastic_store.as_retriever()

retriever = EnsembleRetriever(
    retrievers=[vector_store_retriever, bm25_retriever],
    weights=[0.6, 0.4]
)

docs = retriever.invoke("1С:Бухгалтерия")
print(docs)
