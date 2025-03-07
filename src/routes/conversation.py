from fastapi import APIRouter

from src.eva.conversation_validation import handle_conversation_logic
from src.models.conversation import Conversation

router = APIRouter()


@router.post("/chat/")
async def chat_with_tob(conversation: Conversation) -> dict:
    response_to_user = await handle_conversation_logic(conversation)
    return response_to_user
