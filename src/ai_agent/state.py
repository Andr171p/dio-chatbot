from typing_extensions import TypedDict


class State(TypedDict):
    user_id: str
    user_message: str
    dialog: str
    summarized_message: str
    clarifying_question: str
    context: str
    generation: str
    final_answer: str
