import asyncio

import streamlit as st

from src.di.container import container
from src.core.use_cases import ChatBotUseCase


async def main() -> None:
    chatbot_use_case = await container.get(ChatBotUseCase)
    user_id = "2"
    st.title("ДИО-Чат")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_message = st.text_input("Сообщение:")

    if st.button("Отправить"):
        if user_message:
            st.session_state.chat_history.append({"user": user_message})

            chatbot_message = await chatbot_use_case.answer(user_id, user_message)

            st.session_state.chat_history.append({"chatbot": chatbot_message})

    for chat in st.session_state.chat_history:
        if "user" in chat:
            st.write(f"Вы: {chat["user"]}")
        elif "bot" in chat:
            st.write(f"Бот: {chat["chatbot"]}")


if __name__ == "__main__":
    asyncio.run(main())
