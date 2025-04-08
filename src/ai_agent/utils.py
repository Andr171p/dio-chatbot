from typing import List

from langchain_core.documents import Document


def format_documents(documents: List[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])


def format_messages(user_message: str, messages: List[str]) -> str:
    return f"{"\n".join([message for message in messages])}\nhuman: {user_message}"
