import logging
import aiosqlite
from collections.abc import AsyncGenerator
from typing import Any, List, Optional, Union

from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph.state import CompiledGraph, CompiledStateGraph

# from langchain_core.tools import StructuredTool
from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseChatModel, BaseLLM

from src.ai_agent.base_agent import BaseAgent


log = logging.getLogger(__name__)


class ReACTAgent(BaseAgent):
    def __init__(
            self,
            db_url: str,
            tools: List[BaseTool],
            prompt_template: str,
            model: Union[BaseChatModel, BaseLLM]
    ) -> None:
        self._db_url = db_url
        self._tools = tools
        self._prompt_template = prompt_template
        self._model = model

    def _create_react_agent(self) -> CompiledGraph:
        return create_react_agent(
            tools=self._tools,
            state_modifier=self._prompt_template,
            model=self._model
        )

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(MessagesState)
        graph.add_node("agent", self._create_react_agent())
        graph.add_edge(START, "agent")
        return graph

    async def _build_and_compile_graph(self) -> CompiledStateGraph:
        graph = self._build_graph()
        connection = await aiosqlite.connect(self._db_url)
        checkpointer = AsyncSqliteSaver(connection)
        await checkpointer.setup()
        compiled_graph = graph.compile(checkpointer=checkpointer)
        return compiled_graph

    async def generate(self, thread_id: str, query: str) -> Optional[str]:
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [{"role": "human", "content": query}]}
        compiled_graph = await self._build_and_compile_graph()
        response = await compiled_graph.ainvoke(inputs, config=config)
        print(response)
        message = response.get("messages")[-1]
        return message.content

    async def stream(self, thread_id: str, query: str) -> AsyncGenerator[str, Any]:
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [{"role": "human", "content": query}]}
        compiled_graph = await self._build_and_compile_graph()
        async for event in compiled_graph.astream(inputs, config=config, stream_mode="values"):
            message = event["messages"][-1]
            if isinstance(message, AIMessage):
                message_content = message.content
                yield message_content
