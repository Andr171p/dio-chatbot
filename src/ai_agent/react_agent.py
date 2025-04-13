import logging
import aiosqlite
from collections.abc import AsyncGenerator
from typing import Any, List, Optional, Union

from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.graph.state import CompiledGraph, CompiledStateGraph

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

    async def generate(self, thread_id: str, query: str) -> Optional[str]:
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [{"role": "human", "content": query}]}
        graph = self._build_graph()
        compiled_graph = await self._compile_graph(graph)
        response = await compiled_graph.ainvoke(inputs, config=config)
        print(response)
        message = response.get("messages")[-1]
        return message.content

    async def stream(self, thread_id: str, query: str) -> AsyncGenerator[str, Any]:
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [{"role": "human", "content": query}]}
        graph = self._build_graph()
        compiled_graph = await self._compile_graph(graph)
        async for event in compiled_graph.astream(inputs, config=config, stream_mode="values"):
            message = event["messages"][-1]
            if isinstance(message, AIMessage):
                yield message.content

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

    async def _get_checkpointer(self) -> BaseCheckpointSaver:
        connection = await aiosqlite.connect(self._db_url)
        checkpointer = AsyncSqliteSaver(connection)
        await checkpointer.setup()
        return checkpointer

    async def _compile_graph(self, graph: StateGraph) -> CompiledStateGraph:
        checkpointer = await self._get_checkpointer()
        compiled_graph = graph.compile(checkpointer=checkpointer)
        return compiled_graph
