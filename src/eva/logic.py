import openai
import os

from fastapi import Depends
from openai import OpenAI
from sqlalchemy.orm import Session

from src.config.const import OPENAI_API_KEY
from src.database.add import add_new_message
from src.database.get import get_chat_history
from src.models.conversation import Conversation
import openai




def check_chat_history(conversation_id):
    print("todo lions")
    db_chat=get_chat_history(conversation_id)
    #logic for bd


    return db_chat


def save_response_message(message, response_message):

    add_new_message(message)
    add_new_message(response_message)

    pass


def eva_testmode_01(conversation_id, message):


    client = OpenAI(
        api_key=os.environ.get(OPENAI_API_KEY),

    )
    print("eva_testmode_01")
    debate_history = []

    if conversation_id:

        debate_history =check_chat_history(conversation_id)





    #TODO: validate roles

    system_message = {
        "role": "system",
        "content": "Eres un experto en debates. Siempre argumentas de manera lógica, respetuosa y detallada."
    }
    assistant_message = {
        "role": "assistant",
        "content": "Soy un defensor de la inteligencia artificial. Creo que su impacto en la sociedad será positivo y puede traer grandes beneficios a todos los niveles."
    }
    user_message = {
        "role": "user",
        "content": message
    }
    messages = [system_message, assistant_message] + debate_history + [user_message]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )




    response_message = [{
        "role": "user",
        "message": message

    },{"role": "eva",
       "message":response.choices[0].message.content}]


    save_response_message(message, response.choices[0].message.content)




    return {"response": response_message}

