# src/agno/adapter.py

from agno.agent import Agent
from agno.memory.v2.memory import Memory
from agno.models.openai import OpenAIChat

from src.agno.memory import ExistingMySqlMemoryDb
from src.eva.logic import tob_conversation_logic

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "pass123",
    "database": "kopichallengedb"
}

# Por ahora, usamos mapeo estático entre user_id y conversation_id
USER_CONV_MAP = {
    "christian": 42,
    "peter_rabbit": 7
}


def get_agent(user_id: str) -> Agent:
    memory = Memory(
        db=ExistingMySqlMemoryDb(
            connection_config=MYSQL_CONFIG,
            user_to_conversation_id=USER_CONV_MAP
        ),
        model=OpenAIChat(id="gpt-4o-mini")  # opcional
    )
    return Agent(
        model=None,
        user_id=user_id,
        memory=memory,
        enable_agentic_memory=True,
        markdown=True
    )


def handle_message_with_tob(user_id: str, conversation_id: int, message: str) -> str:
    agent = get_agent(user_id)
    agent.memory.append_message(user_id, role="user", content=message)

    # Tu lógica personalizada
    result = tob_conversation_logic(
        conversation_id=conversation_id,
        validated_message="",
        original_message=message,
        firt_interaction=False
    )

    response_text = result["response"][-1]["message"]
    agent.memory.append_message(user_id, role="assistant", content=response_text)

    return response_text
