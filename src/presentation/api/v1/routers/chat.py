from fastapi import APIRouter, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from src.core.entities import AskingUser
from src.core.use_cases import ChatAssistant
from src.presentation.api.v1.schemas import ChatResponse


chat_router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat with AI assistant"],
    route_class=DishkaRoute
)


@chat_router.post(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=ChatResponse
)
async def answer(
        asking_user: AskingUser,
        chat_assistant: FromDishka[ChatAssistant]
) -> ChatResponse:
    assistant_message = await chat_assistant.answer(**asking_user.model_dump())
    return ChatResponse.from_assistant_message(assistant_message)
