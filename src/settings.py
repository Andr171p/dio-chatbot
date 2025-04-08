import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


class ElasticsearchSettings(BaseSettings):
    url: str = "https://localhost:9200"
    user: str = "elastic"
    password: str = "password"


class PostgresSettings(BaseSettings):
    host: str = os.getenv("PG_HOST")
    port: int = os.getenv("PG_PORT")
    user: str = os.getenv("PG_USER")
    password: str = os.getenv("PG_PASSWORD")
    db: str = os.getenv("PG_DB")

    driver: str = "asyncpg"

    url: str = f"postgresql+{driver}://{user}:{password}@{host}:{port}/{db}?sslmode=disable"


class SQLiteSettings(BaseSettings):
    db_path: str = str(BASE_DIR / "db.sqlite3")
    driver: str = "aiosqlite"
    url: str = f"sqlite:///{db_path}"


class EmbeddingsSettings(BaseSettings):
    model_name: str = "intfloat/multilingual-e5-large"
    model_kwargs: dict[str, str] = {"device": "cpu"}
    encode_kwargs: dict[str, bool] = {"normalize_embeddings": False}


class GigaChatSettings(BaseSettings):
    api_key: str = os.getenv("GIGACHAT_API_KEY")
    scope: str = os.getenv("GIGACHAT_SCOPE")


class YandexGPTSettings(BaseSettings):
    folder_id: str = os.getenv("YANDEX_FOLDER_ID")
    api_key: str = os.getenv("YANDEX_GPT_API_KEY")


class PromptsSettings(BaseSettings):
    system_path: Path = BASE_DIR / "prompts" / "system.txt"
    retrival_description_path: Path = BASE_DIR / "prompts" / "retrieval_description.txt"


class Settings(BaseSettings):
    elasticsearch: ElasticsearchSettings = ElasticsearchSettings()
    postgres: PostgresSettings = PostgresSettings()
    sqlite: SQLiteSettings = SQLiteSettings()
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    giga_chat: GigaChatSettings = GigaChatSettings()
    yandex_gpt: YandexGPTSettings = YandexGPTSettings()
    prompts: PromptsSettings = PromptsSettings()


settings = Settings()
