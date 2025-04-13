from __future__ import annotations

from typing import Any, List, Optional, Union
from functools import cached_property

from pydantic import Field

from langchain_core.tools import BaseTool
from langchain_core.load.serializable import Serializable

from src.llms.yandex_gpt.api import YandexGPTAPI
from src.llms.yandex_gpt.utils import create_tools
from src.llms.yandex_gpt.constants import AVAILABLE_MODELS, URL


class _BaseYandexGPT(Serializable):
    model: AVAILABLE_MODELS = "yandexgpt-lite"
    url: str = URL
    folder_id: Optional[str] = None
    api_key: Optional[str] = None
    iam_token: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    timeout: Optional[int] = None
    tool_choice: Optional[Union[str, dict[str, str]]] = Field(
        default=None,
        description="Controls which tool is called. Set to 'auto' or a specific tool."
    )
    tools: Optional[List[BaseTool]] = Field(
        default=None,
        description="List of tools available to the model for function calling."
    )
    streaming: bool = False

    @property
    def _llm_type(self) -> str:
        return "YandexGPT"

    @property
    def _identifying_params(self) -> dict[str, Any]:
        return {
            "model_uri": self.model_uri,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }

    @property
    def model_uri(self) -> str:
        return f"gpt://{self.folder_id}/{self.model}"

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}",
            "x-folder-id": self.folder_id
        }

    def _payload(
            self,
            messages: List[dict[str, Any]],
            stop: Optional[List[str]] = None,
            **kwargs: Any
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "modelUri": self.model_uri,
            "completionOptions": {
                "temperature": self.temperature,
                "maxTokens": self.max_tokens
            },
            "messages": messages
        }
        if self.tools:
            payload["tools"] = create_tools(self.tools)
        if stop:
            payload["completionOptions"]["stopSequences"] = stop
        payload.update(kwargs)
        return payload

    @property
    def _available_tools(self) -> dict[str, BaseTool]:
        return {tool.name: tool for tool in self.tools}

    @cached_property
    def _yandex_gpt_api(self) -> YandexGPTAPI:
        return YandexGPTAPI(
            url=self.url,
            model=self.model,
            folder_id=self.folder_id,
            api_key=self.api_key,
            iam_token=self.iam_token,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            tools=create_tools(self.tools) if self.tools else None
        )
