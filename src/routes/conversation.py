from fastapi import APIRouter

from src.eva.conversation_validation import handle_conversation_logic
from src.models.conversation import Conversation

router = APIRouter()


@router.post("/chat/")
async def chat_with_tob(conversation: Conversation) -> dict:
    return await handle_conversation_logic(conversation)


'''@router.post("/chat/agno")
async def chat_with_agno(conversation: Conversation) -> dict:
    return await  handle_conversation_for_agno(conversation)'''
