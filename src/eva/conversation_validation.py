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
