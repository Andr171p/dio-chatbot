from typing import Any, List, Optional

import logging

import aiohttp
import requests

from src.yandex_gpt.constants import AVAILABLE_MODELS
from src.yandex_gpt.exceptions import YandexGPTAPIException


logger = logging.getLogger(__name__)


class YandexGPTAPI:
    def __init__(
            self,
            folder_id: str,
            api_key: str,
            url: Optional[str] = None,
            model: AVAILABLE_MODELS = "yandexgpt-lite",
            temperature: Optional[float] = None,
            max_tokens: Optional[int] = None,
            tools: Optional[dict[str, Any]] = None,
            timeout: Optional[int] = None
    ) -> None:
        self._folder_id = folder_id
        self._api_key = api_key
        self._url = url
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._tools = tools
        self._timeout = timeout

    @property
    def _model_uri(self) -> str:
        return f"gpt://{self._folder_id}/{self._model}"

    @property
    def _headers(self) -> dict[str, Any]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self._api_key}",
            "x-folder-id": self._folder_id
        }

    def _payload(
            self,
            messages: List[dict[str, str]],
            stop: Optional[List[str]] = None
    ) -> dict[str, Any]:
        payload = {
            "modelUri": self._model_uri,
            "completionOptions": {
                "temperature": self._temperature,
                "maxTokens": self._max_tokens
            },
            "messages": messages
        }
        if self._tools:
            payload["tools"] = self._tools
        if stop:
            payload["completionOptions"]["stopSequences"] = stop
        return payload

    def complete(
            self,
            messages: List[dict[str, str]],
            stop: Optional[list[str]] = None
    ) -> Optional[dict[str, Any]]:
        try:
            with requests.Session() as session:
                response = session.post(
                    url=self._url,
                    headers=self._headers,
                    json=self._payload(messages, stop),
                    timeout=self._timeout
                )
                response.raise_for_status()
                return response.json()
        except requests.RequestException as ex:
            logger.error("YandexGPT api error %s", ex)
            raise YandexGPTAPIException(ex)

    async def async_complete(
            self,
            messages: List[dict[str, str]],
            stop: Optional[List[str]] = None
    ) -> dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url=self._url,
                        headers=self._headers,
                        json=self._payload(messages, stop),
                        timeout=self._timeout
                ) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as ex:
            logger.error("YandexGPT api error %s", ex)
            raise YandexGPTAPIException(ex)
