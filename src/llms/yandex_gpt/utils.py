from typing import Optional, List

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    FunctionMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)


def get_yandex_message(message: BaseMessage) -> Optional[dict[str, str]]:
    yandex_message: Optional[dict[str, str]] = None
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
