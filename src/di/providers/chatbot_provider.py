from dishka import Provider, provide, Scope

from langchain.retrievers import EnsembleRetriever
from langchain_core.language_models import BaseChatModel

from src.ai_agent.tools import RetrievalTool
from src.ai_agent import BaseAgent, ReACTAgent

from src.core.use_cases import ChatBotUseCase

from src.misc.file_readers import read_txt
from src.settings import settings


class ChatBotProvider(Provider):
    @provide(scope=Scope.APP)
    def get_retrieval_tool(self, retriever: EnsembleRetriever) -> RetrievalTool:
        return RetrievalTool(retriever)

    @provide(scope=Scope.APP)
    def get_react_agent(self, retrieval_node: RetrievalTool, model: BaseChatModel) -> ReACTAgent:
        return ReACTAgent(
            db_url=settings.sqlite.db_path,
            tools=[retrieval_node],
            prompt_template=read_txt(...),
            model=model
        )

    @provide(scope=Scope.APP)
    def get_chatbot_use_case(self, ai_agent: BaseAgent) -> ChatBotUseCase:
        return ChatBotUseCase(ai_agent)
