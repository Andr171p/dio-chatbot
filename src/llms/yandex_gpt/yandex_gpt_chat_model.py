import json

import aiohttp
import requests

from typing import (
    Any,
    List,
    Union,
    Iterator,
    Optional
)

from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage
)
from langchain_core.messages.ai import UsageMetadata
from langchain_core.outputs import (
    ChatGeneration,
    ChatGenerationChunk,
    ChatResult
)
from pydantic import Field

from src.llms.yandex_gpt.consts import AVAILABLE_MODELS
from src.llms.yandex_gpt.utils import get_yandex_messages


class YandexGPTChatModel(BaseChatModel):
    model_name: AVAILABLE_MODELS = "yandexgpt-lite"
    url: str = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    folder_id: Optional[str] = None
    api_key: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    timeout: Optional[int] = None
    tool_choice: Optional[Union[str, dict[str, str]]] = Field(
        default=None,
        description="Controls which tool is called. Set to 'auto' or a specific tool."
    )
    tools: Optional[List[dict]] = Field(
        default=None,
        description="List of tools available to the model for function calling."
    )

    @property
    def model_uri(self) -> str:
        return f"gpt://{self.folder_id}/{self.model_name}"

    @property
    def _headers(self) -> dict[str, Any]:
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
            payload["tools"] = self.tools
        if stop:
            payload["completionOptions"]["stopSequences"] = stop
        payload.update(kwargs)
        return payload

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        yandex_messages = get_yandex_messages(messages)
        print(self._payload(yandex_messages, stop))
        response = requests.post(
            url=self.url,
            headers=self._headers,
            json=self._payload(yandex_messages, stop)
        )
        print(response.json())
        response.raise_for_status()
        data = response.json()

        if "result" not in data:
            raise ValueError("Unexpected response format from YandexGPT API")
        alternatives = data["result"]["alternatives"]
        text = alternatives[0].get("message", {}).get("text", "")
        tool_calls = alternatives[0].get("message", {}).get("toolCallList", {}).get("toolCalls", [])

        additional_kwargs = {}
        if tool_calls:
            additional_kwargs["tool_calls"] = tool_calls

        message = AIMessage(
            content=text,
            additional_kwargs=additional_kwargs
        )
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    def bind_tools(
            self,
            tools: List[Union[dict[str, Any], BaseTool]],
            **kwargs: Any
    ) -> "YandexGPTChatModel":
        yandex_tools: List[dict[str, Any]] = []
        for tool in tools:
            if isinstance(tool, BaseTool):
                yandex_tools.append({
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.args_schema.model_json_schema()
                    }
                })
            else:
                yandex_tools.append(tool)
        self.tools = yandex_tools
        return self

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
