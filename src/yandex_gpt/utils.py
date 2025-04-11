from typing import Any, List

from langchain_core.tools import BaseTool


def get_tool(tool: BaseTool) -> dict[str, Any]:
    return {
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.args_schema.model_json_schema()
        }
    }


def get_tools(tools: List[BaseTool]) -> List[dict[str, Any]]:
    return [get_tool(tool) for tool in tools]
