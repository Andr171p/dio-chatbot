import logging
import aiohttp
import requests

from typing import Any, List, Union, Optional

from pydantic import Field
from langchain_core.tools import BaseTool
from langchain_core.outputs import ChatResult
from langchain_core.messages import BaseMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.callbacks import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun

from src.llms.yandex_gpt.yandex_gpt_tool_caller import YandexGPTToolCaller
from src.llms.yandex_gpt.consts import AVAILABLE_MODELS
from src.llms.yandex_gpt.utils import (
    get_yandex_messages,
    get_yandex_tools,
    get_chat_results_from_yandex_gpt_response
)


log = logging.getLogger(__name__)


class YandexGPTChatModel(YandexGPTToolCaller, BaseChatModel):
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
    tools: Optional[List[BaseTool]] = Field(
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
            payload["tools"] = get_yandex_tools(self.tools)
        if stop:
            payload["completionOptions"]["stopSequences"] = stop
        payload.update(kwargs)
        return payload

    def _generate_chat_result(
            self,
            messages: list[BaseMessage],
            stop: Optional[list[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        yandex_messages = get_yandex_messages(messages)
        response = requests.post(
            url=self.url,
            headers=self._headers,
            json=self._payload(yandex_messages, stop)
        )
        response.raise_for_status()
        data = response.json()

        chat_result = get_chat_results_from_yandex_gpt_response(data)
        print(chat_result)
        return chat_result

    async def _agenerate_chat_result(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        yandex_messages = get_yandex_messages(messages)
        log.info(self._payload(yandex_messages, stop))
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=self.url,
                    headers=self._headers,
                    json=self._payload(yandex_messages, stop)
            ) as response:
                data = await response.json()
        chat_result = get_chat_results_from_yandex_gpt_response(data)
        return chat_result

    def _generate_with_tools(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        chat_result = self._generate_chat_result(messages, stop, run_manager, **kwargs)
        ai_message = chat_result.generations[0].message
        if hasattr(ai_message, "tool_calls") and ai_message.tool_calls:
            tool_message = self._call_tool(ai_message.tool_calls, run_manager)
            messages_with_calling_tool = messages + [ai_message] + tool_message
            chat_result = self._generate_chat_result(messages_with_calling_tool, stop, run_manager, **kwargs)
        return chat_result

    async def _agenerate_with_tools(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        chat_result = await self._agenerate_chat_result(messages, stop, run_manager, **kwargs)
        ai_message = chat_result.generations[0].message
        if hasattr(ai_message, "tool_calls") and ai_message.tool_calls:
            tool_message = await self._acall_tool(ai_message.tool_calls, run_manager)
            messages_with_calling_tool = messages + [ai_message] + tool_message
            chat_result = await self._agenerate_chat_result(messages_with_calling_tool, stop, run_manager, **kwargs)
        return chat_result

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.tools:
            return self._generate_with_tools(messages, stop, run_manager, **kwargs)
        return self._generate_chat_result(messages, stop, run_manager, **kwargs)

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.tools:
            return await self._agenerate_with_tools(messages, stop, run_manager, **kwargs)
        return await self._agenerate_chat_result(messages, stop, run_manager, **kwargs)

    def bind_tools(
            self,
            tools: List[Union[dict[str, Any], BaseTool]],
            **kwargs: Any
    ) -> "YandexGPTChatModel":
        self.tools = tools
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
