from fastapi import APIRouter
from src.models.conversation import Conversation
router = APIRouter()
@router.post("/chat/eva")
async def chat(conversation: Conversation):
    print(conversation)

    return {"message": "Message received successfully"}