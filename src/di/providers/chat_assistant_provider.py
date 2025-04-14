from dishka import Provider, provide, Scope

from langchain.retrievers import EnsembleRetriever
from langchain_core.language_models import BaseChatModel

from src.ai_agent import BaseAgent, ReACTAgent

from src.core.use_cases import ChatAssistant
from src.ai_agent.tools import RetrievalTool, SearchProductTool

from src.misc.files import read_txt
from src.settings import settings


class ChatBotProvider(Provider):
    @provide(scope=Scope.APP)
    def get_retrieval_tool(self, retriever: EnsembleRetriever) -> RetrievalTool:
        return RetrievalTool(retriever)

    @provide(scope=Scope.APP)
    def get_search_product_tool(self) -> SearchProductTool:
        return SearchProductTool(settings.files.price_list_path)

    @provide(scope=Scope.APP)
    def get_react_agent(
            self,
            retrieval_tool: RetrievalTool,
            search_product_tool: SearchProductTool,
            model: BaseChatModel
    ) -> BaseAgent:
        return ReACTAgent(
            db_url=settings.sqlite.db_path,
            tools=[retrieval_tool, search_product_tool],
            prompt_template=read_txt(settings.prompts.system_path),
            model=model
        )

    @provide(scope=Scope.APP)
    def get_chat_assistant(self, ai_agent: BaseAgent) -> ChatAssistant:
        return ChatAssistant(ai_agent)
