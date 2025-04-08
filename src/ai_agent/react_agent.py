import sqlite3
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, List, Optional, Union

from langgraph.prebuilt import create_react_agent
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.graph.state import CompiledGraph, CompiledStateGraph
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from langchain_core.tools import StructuredTool
from langchain_core.language_models import BaseChatModel, BaseLLM


log = logging.getLogger(__name__)


class ReACTAgent:
    def __init__(
            self,
            db_url: str,
            tools: List[StructuredTool],
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
            prompt=self._prompt_template,
            model=self._model
        )

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(MessagesState)
        graph.add_node("agent", self._create_react_agent())
        graph.add_edge(START, "agent")
        return graph

    async def _compile_graph(self) -> CompiledStateGraph:
        graph = self._build_graph()
        saver = AsyncSqliteSaver(sqlite3.connect(self._db_url))
        await saver.setup()
        compiled_graph = graph.compile()
        return compiled_graph

    async def stream(self, thread_id: str, query: str) -> Optional[str]:
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [{"role": "human", "content": query}]}
        compiled_graph = await self._compile_graph()
        async for event in compiled_graph.astream(inputs, config=config, stream_mode="values"):
            message = event["messages"][-1]
            print(message)
