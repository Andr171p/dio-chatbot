from __future__ import annotations

from typing import Any, List, Optional, Union

from pydantic import Field

from langchain_core.tools import BaseTool
from langchain_core.load.serializable import Serializable

from src.yandex_gpt.constants import AVAILABLE_MODELS, URL
from src.yandex_gpt.utils import create_tools


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
        return f"gpt://{self.folder_id}/{self.model_name}"

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
