from typing import Annotated, Sequence
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class State(TypedDict):
    user_id: str
    user_message: str
    dialog: str
    summarized_message: str
    clarifying_question: str
    context: str
    generation: str
    final_answer: str


class MessagesState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
