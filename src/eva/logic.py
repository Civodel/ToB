import os

from openai import OpenAI

from src.config.const import OPENAI_API_KEY, PROMPT_SYSTEM, PROMPT_ASSISTANT
from src.database.add import add_new_message, add_new_conversation
from src.database.get import get_chat_history, get_last_chat
from src.eva.validation import valid_final_response


def create_conversation(message):
    print(message)
    new_conversation = add_new_conversation(message)

    print(new_conversation)

    return new_conversation["conversation_id"]


def check_chat_history(conversation_id):
    history_db = []

    db_chat = get_chat_history(conversation_id)

    for chat in db_chat:
        conversacion_dict = {k: v for k, v in vars(chat).items() if k != "_sa_instance_state"}

        history_db.append(conversacion_dict)

    return history_db


def save_response_message(message, user, response_message, bot, conversation_id):
    add_new_message(message, conversation_id, user)
    add_new_message(response_message, conversation_id, bot)

    pass


def eva_testmode_01(conversation_id, message, original_message):
    client = OpenAI(
        api_key=os.environ.get(OPENAI_API_KEY),

    )

    debate_history = []
    his_msg = []
    debate_history_messages = check_chat_history(conversation_id)

    for regis in debate_history_messages:
        if regis["usuario"] == "eva":
            role = "assistant"
        else:
            role = "user"

        debate_history.append({"role": role, "content": regis["mensaje"]})
    # TODO: validate roles

    user_final_message = original_message if message == '' else original_message
    system_message = {
        "role": "system",
        "content": PROMPT_SYSTEM
    }
    assistant_message = {
        "role": "assistant",
        "content": PROMPT_ASSISTANT
    }
    user_message = {
        "role": "user",
        "content": f"menssaje del cliente: {user_final_message}\n\n"
    }
    messages = [system_message, assistant_message] + debate_history + [user_message]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=50,
        temperature=0.7,
        top_p=0.95
    )

    message_history = get_last_chat(conversation_id)

    if message_history:
        for msg in message_history:
            mssg_dict = {k: v for k, v in vars(msg).items() if k != "_sa_instance_state"}

            evangelion = {
                "role": mssg_dict["usuario"],
                "message": mssg_dict["mensaje"]
            }

            his_msg.append(evangelion)

    final_model_test = valid_final_response(response.choices[0].message.content)

    response_message = [
        {"conversation_id": conversation_id},

        his_msg, {
            "role": "user",
            "message": original_message

        }, {"role": "eva",
            "message": final_model_test}]

    save_response_message(message, "user", final_model_test, "eva", conversation_id)

    return {"response": response_message}
