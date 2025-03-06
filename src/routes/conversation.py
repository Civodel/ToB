from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Conversacion as dbConverssation
from src.eva.logic import eva_testmode_01, create_conversation
from src.eva.validation import valid_user_input
from src.models.conversation import Conversation

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

    db_conversation = db.query(dbConverssation).filter(
        dbConverssation.conversation_id == conversation.conversation_id).first()

    print(db_conversation)

    return {"message": "Messages received successfully"}


def combine_responses(openai_response: str) -> str:
    # Puedes hacer una combinación más compleja o lógica para fusionar las respuestas

    return f"OpenAI dice: {openai_response}\n"


@router.post("/chat/")
async def chat(conversation: Conversation):
    acceptable_user_message = ''
    if not conversation.conversation_id:
        acceptable_user_message, validate_message = valid_user_input(conversation.message)

        if acceptable_user_message == False:
            return validate_message

        else:
            conversation_id = create_conversation(conversation.message)
    else:
        conversation_id = conversation.conversation_id

    return eva_testmode_01(conversation_id, acceptable_user_message, conversation.message)
