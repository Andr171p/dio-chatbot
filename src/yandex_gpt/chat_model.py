import logging

from typing import Any, List, Optional

from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.callbacks import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun

from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import ToolMessage, BaseMessage, AIMessage

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
        print(response)
        chat_result = create_chat_result(response)
        if self.tools:
            ai_message = chat_result.generations[0].message
            print(ai_message)
            if ai_message.tool_calls:
                print(ai_message.tool_calls)
                tool_messages = self._call_tool(ai_message.tool_calls)
                messages_with_called_tools = messages + [ai_message] + tool_messages
                response = self._yandex_gpt_api.complete(create_messages(messages_with_called_tools), stop)
                chat_result = create_chat_result(response)
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
            tool_messages = await self._acall_tool(ai_message.additional_kwargs.get("tool_calls"))
            messages_with_calling_tools = messages + [ai_message] + tool_messages
            response = await self._yandex_gpt_api.acomplete(create_messages(messages_with_calling_tools), stop)
            chat_result = create_chat_result(response)
        return chat_result

    def bind_tools(self, tools: List[BaseTool], **kwargs: Any) -> "YandexGPTChatModel":
        self.tools = tools
        return self

    def _call_tool(self, tool_calls: List[dict]) -> List[ToolMessage]:
        tool_messages: List[ToolMessage] = []
        for tool_call in tool_calls:
            tool_name: str = tool_call["name"]
            tool_args: dict[str, Any] = tool_call.get("args")
            if tool_name in self._available_tools:
                logger.info("Calling tool: %s with args: %s", tool_name, tool_args)
                tool = self._available_tools[tool_name]
                content = tool.invoke(tool_args["input"])
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


from langchain_core.tools import tool


@tool
def magic_words(username: str) -> str:
    """answer a dynamic password if user want to know magic words

    Args:
        username: name of user, or "<UNKNOWN>" if you don't know the username.
    """
    mw = "xxxxxxxxxx" + username
    print(mw)
    return mw

from src.settings import settings

model = YandexGPTChatModel(
    model="yandexgpt",
    api_key=settings.yandex_gpt.api_key,
    folder_id=settings.yandex_gpt.folder_id
)

model.bind_tools([magic_words])

print(model.invoke("Какие у тебя есть инстументы"))
