import logging

from typing import Any, List, Optional

from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.callbacks import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun

from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import ToolMessage, BaseMessage

from src.yandex_gpt.base import _BaseYandexGPT
from src.yandex_gpt.utils import create_messages, create_chat_result


logger = logging.getLogger(__name__)


class YandexGPTChatModel(_BaseYandexGPT, BaseChatModel):
    def _generate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        response = self._yandex_gpt_api.complete(create_messages(messages), stop)
        chat_result = create_chat_result(response)
        if self.tools:
            ai_message = chat_result.generations[0].message
            tool_message = self._call_tool(ai_message.additional_kwargs.get("tool_calls"))
            generation = ChatGeneration(message=tool_message[0])
            chat_result = ChatResult(generations=[generation])
        return chat_result

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: Optional[list[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        response = await self._yandex_gpt_api.acomplete(create_messages(messages), stop)
        chat_result = create_chat_result(response)
        if self.tools:
            ai_message = chat_result.generations[0].message
            tool_message = await self._acall_tool(ai_message.additional_kwargs.get("tool_calls"))
            generation = ChatGeneration(message=tool_message[0])
            chat_result = ChatResult(generations=[generation])
        return chat_result

    def bind_tools(self, tools: List[BaseTool], **kwargs: Any) -> "YandexGPTChatModel":
        self.tools = tools
        return self

    def _call_tool(self, tool_calls: List[dict]) -> List[ToolMessage]:
        tool_messages: List[ToolMessage] = []
        for tool_call in tool_calls:
            tool_name: str = tool_call["functionCall"]["name"]
            tool_args: dict[str, Any] = tool_call["functionCall"].get("arguments")
            if tool_name in self._available_tools:
                logger.info("Calling tool: %s with args: %s", tool_name, tool_args)
                tool = self._available_tools[tool_name]
                content = tool.invoke(tool_args)
                tool_messages.append(
                    ToolMessage(
                        content=str(content),
                        tool_call_id=tool_call.get("id", ""),
                        name=tool_name
                    )
                )
        return tool_messages

    async def _acall_tool(self, tool_calls: List[dict]) -> List[ToolMessage]:
        tool_messages: List[ToolMessage] = []
        for tool_call in tool_calls:
            tool_name: str = tool_call["functionCall"]["name"]
            tool_args: dict[str, Any] = tool_call["functionCall"].get("arguments")
            if tool_name in self._available_tools:
                logger.info("Calling tool: %s with args: %s", tool_name, tool_args)
                tool = self._available_tools[tool_name]
                content = await tool.arun(tool_args)
                tool_messages.append(
                    ToolMessage(
                        content=str(content),
                        tool_call_id=tool_call.get("id", ""),
                        name=tool_name
                    )
                )
        return tool_messages
