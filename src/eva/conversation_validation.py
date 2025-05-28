from src.eva.logic import create_conversation, tob_conversation_logic
from src.eva.validation import valid_user_input
from src.models.conversation import Conversation


async def handle_conversation_logic(conversation: Conversation) -> dict:
    acceptable_user_message = False
    first_interaction = False
    validate_message = ''
    if not conversation.conversation_id:

        acceptable_user_message, validate_message = valid_user_input(conversation.message)

        if acceptable_user_message is False:
            return {'ToB': validate_message}

        conversation_id = create_conversation(conversation.message)
        first_interaction = True
    else:
        conversation_id = conversation.conversation_id

    return tob_conversation_logic(conversation_id, validate_message, conversation.message, first_interaction)




'''async def handle_conversation_for_agno(conversation: Conversation) -> dict:
    print("entrando en la funcion")

    acceptable_user_message = False
    first_interaction = False
    validate_message = ''

    if not conversation.conversation_id:
        # 🧠 Validar input del usuario
        acceptable_user_message, validate_message = valid_user_input(conversation.message)

        if acceptable_user_message is False:
            return {'ToB': validate_message}

        # 🧠 Crear conversación nueva
        conversation_id = create_conversation(conversation.message)
        first_interaction = True

        # 💥 Agno: limpiar memoria si existe
        user_id = f"{conversation.user_id}_{conversation_id}"
        agent = get_agent(user_id)
        agent.memory.clear()  # nueva conversación = memoria nueva
    else:
        conversation_id = conversation.conversation_id
        user_id = f"{conversation.user_id}_{conversation_id}"

    # 💬 Ejecutar ToB como siempre
    response = tob_conversation_logic(
        conversation_id,
        validate_message,
        conversation.message,
        first_interaction
    )

    # 🧠 Guardar en memoria de Agno (si quieres)
    agent = get_agent(user_id)
    agent.memory.db.add_message(user_id, role="user", content="mensaje")
    agent.memory.db.add_message(user_id, role="assistant", content=response["response"][-1]["message"])

    return response
'''