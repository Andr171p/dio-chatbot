from typing import Any, Optional, List

from langchain_core.tools import BaseTool
from langchain_core.outputs import (
    ChatResult,
    ChatGeneration
)
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage
)


def fill_empty_message_content(message: BaseMessage) -> ...:
    if len(message.content) == 0:
        message.content = "Пустое сообщение"
    return message


def get_yandex_message(message: BaseMessage) -> Optional[dict[str, str]]:
    yandex_message: Optional[dict[str, str]] = None
    message = fill_empty_message_content(message)
    if isinstance(message, HumanMessage):
        yandex_message = {"role": "user", "text": message.content}
    elif isinstance(message, AIMessage):
        yandex_message = {"role": "assistant", "text": message.content}
    elif isinstance(message, SystemMessage):
        yandex_message = {"role": "system", "text": message.content}
    elif isinstance(message, ToolMessage):
        yandex_message = {
            "role": "tool",
            "text": message.content,
            "tool_call_id": message.additional_kwargs.get("tool_call_id", "")
        }
    return yandex_message


def get_yandex_messages(messages: List[BaseMessage]) -> List[dict[str, str]]:
    return [get_yandex_message(message) for message in messages]


def get_yandex_tool(tool: BaseTool) -> dict[str, Any]:
    return {
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.args_schema.model_json_schema()
        }
    }


def get_yandex_tools(tools: List[BaseTool]) -> List[dict[str, Any]]:
    return [get_yandex_tool(tool) for tool in tools]


def get_chat_results_from_yandex_gpt_response(response: dict) -> ChatResult:
    if "result" not in response:
        raise ValueError("Unexpected response format from YandexGPT API")
    alternatives = response["result"]["alternatives"]
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
