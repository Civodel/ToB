from fastapi import APIRouter, Depends
from openai import OpenAI
import torch

from src.eva.logic import eva_testmode_01
from src.models.conversation import Conversation
from sqlalchemy.orm import Session
from src.database.db  import get_db
from src.database.models import Conversacion as dbConverssation
import openai
import os
from transformers import pipeline
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import transformers

from src.config.const import MODEL_NAME,OPENAI_API_KEY
from transformers import AutoTokenizer, AutoModelForCausalLM



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


def combine_responses(openai_response: str) -> str:
    # Puedes hacer una combinación más compleja o lógica para fusionar las respuestas

    return f"OpenAI dice: {openai_response}\n"


@router.post("/chat/")
async def chat(conversation: Conversation):
    # TODO valdiate entry for user

    print("todo tigre")
    return eva_testmode_01(conversation.conversation_id,conversation.message)

