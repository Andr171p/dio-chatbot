import uuid

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


def __fill_empty_message_content(message: BaseMessage) -> BaseMessage:
    if len(message.content) == 0:
        message.content = "Пустое сообщение"
    return message


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
    """Convert Langchain message to YandexGPT API format"""
    message = __fill_empty_message_content(message)
    json_message: Optional[dict[str, Any]] = None
    text = message.content
    if isinstance(message, SystemMessage):
        json_message = {"role": "system", "text": text}
    elif isinstance(message, HumanMessage):
        json_message = {"role": "user", "text": text}
    elif isinstance(message, AIMessage):
        json_message = {"role": "assistant", "text": text}
        if hasattr(message, "tool_calls") and message.tool_calls:
            json_message["toolCallList"] = {
                "toolCalls": [
                    {
                        "functionCall": {
                            "name": tool_call["name"],
                            "arguments": tool_call["args"]
                        }
                    }
                    for tool_call in message.tool_calls
                ]
            }
    elif isinstance(message, ToolMessage):
        json_message = {
            "role": "assistant",
            "toolResultList": {
                "toolResults": [
                    {
                        "functionResult": {
                            "name": message.name if hasattr(message, "name") else "unknown",
                            "content": message.content
                        }
                    }
                ]
            }
        }
    return json_message


def create_messages(messages: List[BaseMessage]) -> List[dict[str, str]]:
    return [__create_message(message) for message in messages]


def __convert_tool(tool: BaseTool) -> dict[str, Any]:
    """Convert Langchain tool to YandexGPT API format"""
    parameters = {}
    if tool.args_schema:
        schema = tool.args_schema.model_json_schema()
        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }
        for name, property in schema.get("properties", {}).items():
            parameters["properties"][name] = {
                "type": property.get("type", "string"),
                "description": property.get("description", "")
            }

            if name in schema.get("required", []):
                parameters["required"].append(name)
    else:
        parameters = {
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "Tool input"}
            },
            "required": ["input"]
        }
    return {
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": parameters
        }
    }


def convert_tools(tools: List[BaseTool]) -> List[dict[str, Any]]:
    return [__convert_tool(tool) for tool in tools]


def __parse_response(response: dict[str, Any]) -> AIMessage:
    """Parse YandexGPT API response to Langchain AIMessage"""
    alternative = response["result"]["alternatives"][0]
    if alternative.get("status") == "ALTERNATIVE_STATUS_TOOL_CALLS":
        tool_calls = []
        for tool_call in alternative["message"]["toolCallList"]["toolCalls"]:
            tool_args = {"input": tool_call["functionCall"]["arguments"]}
            tool_calls.append({
                "name": tool_call["functionCall"]["name"],
                "args": tool_args,
                "id": str(uuid.uuid4())
            })
        return AIMessage(
            content="",
            tool_calls=tool_calls,
            additional_kwargs={
                "raw_response": response
            }
        )
    else:
        return AIMessage(
            content=alternative["message"]["text"],
            additional_kwargs={
                "raw_response": response
            }
        )


def create_chat_result(response: dict[str, Any]) -> ChatResult:
    ai_message = __parse_response(response)
    generation = ChatGeneration(message=ai_message)
    return ChatResult(generations=[generation])
