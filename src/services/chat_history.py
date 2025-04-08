import json

from typing import Any, List, Optional

from src.redis import RedisClient


class ChatHistory:
    def __init__(self, connection_params: dict[str, Any]) -> None:
        self.__connection_params = connection_params

    async def save_message(self, user_id: str, message: dict[str, str]) -> None:
        async with RedisClient(**self.__connection_params) as redis_client:
            await redis_client.push_list(user_id, str(message))

    async def get_messages(self, user_id: str, limit: int = 5) -> List[Optional[str]]:
        async with RedisClient(**self.__connection_params) as redis_client:
            messages = await redis_client.read_list(user_id, 0, limit)
        return [json.load(message) for message in messages] if messages else []
