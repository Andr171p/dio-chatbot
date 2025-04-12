from typing import Any, List, Optional

from langchain_core.tools import BaseTool
from langchain_core.outputs import (
    ChatResult,
    ChatGeneration
)
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)


def __create_tool(tool: BaseTool) -> dict[str, Any]:
    return {
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.args_schema.model_json_schema()
        }
    }


def create_tools(tools: List[BaseTool]) -> List[dict[str, Any]]:
    return [__create_tool(tool) for tool in tools]


def __create_message(message: BaseMessage) -> dict[str, str]:
    json_message: Optional[dict[str, str]] = None
    text = message.content
    if isinstance(message, SystemMessage):
        json_message = {"role": "system", "text": text}
    elif isinstance(message, HumanMessage):
        json_message = {"role": "user", "text": text}
    elif isinstance(message, AIMessage):
        json_message = {"role": "assistant", "text": text}
    elif isinstance(message, ToolMessage):
        json_message = {
            "role": "tool",
            "text": text,
            "tool_call_id": message.additional_kwargs.get("tool_call_id", "")
        }
    return json_message


def create_messages(messages: List[BaseMessage]) -> List[dict[str, str]]:
    return [__create_message(message) for message in messages]


def create_chat_result(response: dict[str, Any]) -> ChatResult:
    generations: List[ChatGeneration] = []
    if "result" not in response:
        raise ValueError("Unexpected response format from YandexGPT API")
    alternatives = response["result"]["alternatives"]
    for alternative in alternatives:
        text = alternative.get("message", {}).get("text", "")
        tool_calls = alternative.get("message", {}).get("toolCallList", {}).get("toolCalls", [])
        additional_kwargs = {}
        if tool_calls:
            additional_kwargs["tool_calls"] = tool_calls
        message = AIMessage(
            content=text,
            additional_kwargs=additional_kwargs
        )
        generation = ChatGeneration(message=message)
        generations.append(generation)
    return ChatResult(generations=generations)
