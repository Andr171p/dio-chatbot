import json
import logging

from typing import List, Optional

from langchain_core.tools import BaseTool
from langchain_core.messages import ToolMessage
from langchain_core.callbacks import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun


log = logging.getLogger(__name__)


class YandexGPTToolCaller:
    tools: Optional[List[BaseTool]]

    def __get_available_tools(self) -> dict[str, BaseTool]:
        return {tool.name: tool for tool in self.tools}

    def _call_tool(
            self,
            tool_calls: List[dict],
            run_manager: Optional[CallbackManagerForLLMRun] = None
    ) -> List[ToolMessage]:
        tool_messages: List[ToolMessage] = []
        available_tools = self.__get_available_tools()
        for tool_call in tool_calls:
            tool_name = tool_call.get("functionCall").get("name")
            tool_args = tool_call.get("functionCall").get("arguments", {})
            if isinstance(tool_args, str):
                tool_args = json.loads(tool_args)
            if tool_name in available_tools:
                log.info("Calling tool: %s with args: %s", tool_name, tool_args)
                tool = available_tools[tool_name]
                tool_result = tool.run(tool_args)
                tool_messages.append(
                    ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_call.get("id", ""),
                        name=tool_name,
                    )
                )
        return tool_messages

    async def _acall_tool(
            self,
            tool_calls: List[dict],
            run_manager: Optional[AsyncCallbackManagerForLLMRun] = None
    ) -> List[ToolMessage]:
        tool_messages: List[ToolMessage] = []
        available_tools = self.__get_available_tools()
        for tool_call in tool_calls:
            tool_name = tool_call.get("functionCall").get("name")
            tool_args = tool_call.get("functionCall").get("arguments", {})
            if isinstance(tool_args, str):
                tool_args = json.loads(tool_args)
            if tool_name in available_tools:
                log.info("Calling tool: %s with args: %s", tool_name, tool_args)
                tool = available_tools[tool_name]
                tool_result = await tool.arun(tool_args)
                tool_messages.append(
                    ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_call.get("id", ""),
                        name=tool_name,
                    )
                )
        return tool_messages
