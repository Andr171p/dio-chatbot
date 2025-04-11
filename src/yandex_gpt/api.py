from typing import Any, List, Optional

import logging
import asyncio

import aiohttp
import requests

from src.yandex_gpt.constants import AVAILABLE_MODELS
from src.yandex_gpt.exceptions import YandexGPTAPIException


logger = logging.getLogger(__name__)


class YandexGPTAPI:
    def __init__(
            self,
            folder_id: str,
            api_key: Optional[str] = None,
            iam_token: Optional[str] = None,
            url: Optional[str] = None,
            model: AVAILABLE_MODELS = "yandexgpt-lite",
            temperature: Optional[float] = None,
            max_tokens: Optional[int] = None,
            tools: Optional[dict[str, Any]] = None,
            stream: bool = False,
            timeout: Optional[int] = None
    ) -> None:
        self._folder_id = folder_id
        self._api_key = api_key
        self._iam_token = iam_token
        self._url = url
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._tools = tools
        self._stream = stream
        self._timeout = timeout

    @property
    def _model_uri(self) -> str:
        return f"gpt://{self._folder_id}/{self._model}"

    @property
    def _headers(self) -> dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "x-folder-id": self._folder_id
        }
        if self._api_key:
            headers["Authorization"] = f"Api-Key {self._api_key}"
        elif self._iam_token:
            headers["Authorization"] = f"Bearer {self._iam_token}"
        return headers

    def _payload(
            self,
            messages: List[dict[str, str]],
            stop: Optional[List[str]] = None
    ) -> dict[str, Any]:
        payload = {
            "modelUri": self._model_uri,
            "completionOptions": {
                "stream": self._stream,
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

    async def _send_async_request(
            self,
            messages: List[dict[str, str]],
            stop: Optional[List[str]] = None,
            async_timeout: float = 0.5
    ) -> Optional[dict[str, str]]:
        if not self._iam_token:
            raise YandexGPTAPIException("IAM-TOKEN is required")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=self._url,
                    headers=self._headers,
                    json=self._payload(messages, stop)
                ) as response:
                    data = await response.json()
            operation_id = data["id"]
            done = data["done"]
            while done is False:
                status_operation = await self._get_status_operation(operation_id)
                await asyncio.sleep(async_timeout)
                done = status_operation["done"]
                logger.info("Status operation is %s", done)
                if done is True:
                    return status_operation
        except aiohttp.ClientError as ex:
            logger.error("Error while send async request to YandexGPT: %s", ex)

    async def _get_status_operation(self, operation_id: str) -> Optional[dict[str, Any]]:
        try:
            url = f"{self._url}/{operation_id}"
            headers = {"Authorization": f"Bearer {self._iam_token}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=url,
                    headers=headers
                ) as response:
                    return await response.json()
        except aiohttp.ClientError as ex:
            logger.error("Error while get status of operation: %s", ex)
