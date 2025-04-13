from dishka import Provider, provide, Scope

from langchain.retrievers import EnsembleRetriever
from langchain_core.language_models import BaseChatModel
from langchain.tools.retriever import create_retriever_tool
from langchain.tools import Tool

from src.ai_agent import BaseAgent, ReACTAgent

from src.core.use_cases import ChatAssistant

from src.misc.file_readers import read_txt
from src.settings import settings


class ChatBotProvider(Provider):
    @provide(scope=Scope.APP)
    def get_retrieval_tool(self, retriever: EnsembleRetriever) -> Tool:
        # return RetrievalTool(retriever)
        return create_retriever_tool(
            retriever=retriever,
            name="DIOConsultPricesRetriever",
            description=read_txt(settings.prompts.retrival_description_path)
        )

    @provide(scope=Scope.APP)
    def get_react_agent(self, retrieval_tool: Tool, model: BaseChatModel) -> BaseAgent:
        return ReACTAgent(
            db_url=settings.sqlite.db_path,
            tools=[retrieval_tool],
            prompt_template=read_txt(settings.prompts.system_path),
            model=model
        )

    @provide(scope=Scope.APP)
    def get_chat_assistant(self, ai_agent: BaseAgent) -> ChatAssistant:
        return ChatAssistant(ai_agent)
