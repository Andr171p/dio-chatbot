from typing import Any, List, Optional

import time
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
        else:
            raise ValueError("IAM-TOKEN or API-KEY is not set")
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
            stop: Optional[List[str]] = None
    ) -> Optional[dict[str, Any]]:
        if self._iam_token:
            return self._send_async_request(messages, stop)
        return self._send_request(messages, stop)

    async def acomplete(
            self,
            messages: List[dict[str, str]],
            stop: Optional[List[str]] = None
    ) -> Optional[dict[str, Any]]:
        if self._iam_token:
            return await self._asend_async_request(messages, stop)
        return await self._asend_request(messages, stop)

    def _send_request(
            self,
            messages: List[dict[str, str]],
            stop: Optional[List[str]] = None
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
            logger.error("YandexGPTAPI while send request error %s", ex)
            raise YandexGPTAPIException(ex)

    async def _asend_request(
            self,
            messages: List[dict[str, str]],
            stop: Optional[List[str]] = None
    ) -> Optional[dict[str, Any]]:
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
            logger.error("YandexGPTAPI while send request error %s", ex)
            raise YandexGPTAPIException(ex)

    def _send_async_request(
            self,
            messages: List[dict[str, str]],
            stop: Optional[List[str]] = None,
            async_timeout: float = 0.5
    ) -> Optional[dict[str, Any]]:
        if not self._iam_token:
            raise YandexGPTAPIException("IAM-TOKEN is required")
        try:
            with requests.Session() as session:
                response = session.post(
                    url=self._url,
                    headers=self._headers,
                    json=self._payload(messages, stop)
                )
                data = response.json()
            operation_id: str = data["id"]
            while True:
                status_operation = self._get_status_operation(operation_id)
                time.sleep(async_timeout)
                done: bool = status_operation["done"]
                logger.info("Status operation is %s", done)
                if done is True:
                    return status_operation
        except requests.RequestException as ex:
            logger.error("YandexGPTAPI error while send async request: %s", ex)

    async def _asend_async_request(
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
            operation_id: str = data["id"]
            while True:
                status_operation = await self._aget_status_operation(operation_id)
                await asyncio.sleep(async_timeout)
                done = status_operation["done"]
                logger.info("Status operation is %s", done)
                if done is True:
                    return status_operation
        except aiohttp.ClientError as ex:
            logger.error("Error while send async request to YandexGPT: %s", ex)
            raise YandexGPTAPIException(ex)

    def _get_status_operation(self, operation_id: str) -> Optional[dict[str, Any]]:
        try:
            url = f"{self._url}/{operation_id}"
            headers = {"Authorization": f"Bearer {self._iam_token}"}
            with requests.Session() as session:
                response = session.get(url=url, headers=headers)
                return response.json()
        except requests.RequestException as ex:
            logger.error("Error while get status of operation: %s", ex)
            raise YandexGPTAPIException(ex)

    async def _aget_status_operation(self, operation_id: str) -> Optional[dict[str, Any]]:
        try:
            url = f"{self._url}/{operation_id}"
            headers = {"Authorization": f"Bearer {self._iam_token}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=headers) as response:
                    return await response.json()
        except aiohttp.ClientError as ex:
            logger.error("Error while get status of operation: %s", ex)
            raise YandexGPTAPIException(ex)
