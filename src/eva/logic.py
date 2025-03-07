import logging
import os

from openai import OpenAI

from src.config.const import OPENAI_API_KEY, PROMPT_SYSTEM, PROMPT_ASSISTANT
from src.database.add import add_new_message, add_new_conversation
from src.database.get import get_chat_history, get_last_chat


def create_conversation(message: str) -> int:
    new_conversation = add_new_conversation(message)
    return new_conversation["conversation_id"]


def check_chat_history(conversation_id: int):
    history_db = []

    db_chat = get_chat_history(conversation_id)

    for chat in db_chat:
        conversacion_dict = {k: v for k, v in vars(chat).items() if k != "_sa_instance_state"}

        history_db.append(conversacion_dict)

    return history_db


def save_response_message(message: str, user: str, response_message: str, bot: str, conversation_id: int) -> None:
    add_new_message(message, conversation_id, user)
    add_new_message(response_message, conversation_id, bot)

    pass


client = OpenAI(
    api_key=os.environ.get(OPENAI_API_KEY),
)


def tob_conversation_logic(conversation_id: int, validated_message: str, original_message: str,
                           firt_interaction: bool) -> dict:
    debate_history_messages = check_chat_history(conversation_id) or []
    his_msg = []
    debate_history = [
        {"role": "assistant" if regis["usuario"] == "eva" else "user", "content": regis["mensaje"]}
        for regis in debate_history_messages
    ]

    if validated_message == '':
        user_message = original_message
    else:
        user_message = validated_message

    messages = [
        {"role": "system", "content": PROMPT_SYSTEM},
        {"role": "assistant", "content": PROMPT_ASSISTANT},
        *debate_history[-10:],
        {"role": "user", "content": f"Mensaje del usuario : {user_message}"}
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=80,
            temperature=0.7,
            top_p=0.95
        )
    except Exception as e:
        logging.error(f"Error en la API de OpenAI:: {e}")
        return {"error": "Hubo un problema al interactuar con la API de OpenAI"}
    try:
        message_history = get_last_chat(conversation_id) or []
        his_msg = [{"role": msg.usuario, "message": msg.mensaje} for msg in message_history]
    except Exception as e:
        logging.error(f"Error al guardar el mensaje: {e}")
        return {"error": "No se pudo obtener el historial de mensajes"}

    final_model_test = response.choices[0].message.content

    '''if firt_interaction == False:
        print('second call')
        final_model_test = valid_final_response(response.choices[0].message.content, user_message)'''
    try:
        save_response_message(original_message, "user", final_model_test, "eva", conversation_id)
    except Exception as e:
        logging.error(f"Error al obtener el historial de conversación: {e}")
        return {"error": "No se pudo guardar el mensaje"}
    return {
        "response": [
            {"conversation_id": conversation_id},
            his_msg,
            {"role": "user", "message": original_message},
            {"role": "ToB", "message": final_model_test}
        ]
    }
