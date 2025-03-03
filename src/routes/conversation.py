from fastapi import APIRouter, Depends
from src.models.conversation import Conversation
from sqlalchemy.orm import Session
from src.database.db  import get_db
from src.database.models import Conversacion as dbConverssation

router = APIRouter()
@router.post("/chat/eva")
async def chat(conversation: Conversation):
    print(conversation)

    return {"message": "Message received successfully 2"}


@router.post("/chat/message_test")
async def message_test(conversation: Conversation, db: Session = Depends(get_db)):
    print("holas")

    print(conversation)
    print(conversation.conversation_id)

    db_conversation = db.query(dbConverssation).filter(dbConverssation.conversation_id == conversation.conversation_id).first()

    print(db_conversation)

    return {"message": "Messages received successfully"}