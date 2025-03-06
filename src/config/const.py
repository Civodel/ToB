import os

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSSEEK_API_KEY = os.getenv("DEEPSSEEK_API_KEY")
# Configuración general del chatbot
BOT_NAME = "ChatBot"
DEFAULT_RESPONSE = "No entendí tu mensaje. ¿Puedes reformularlo?"
MAX_HISTORY_MESSAGES = 5
MODEL_NAME = "test"

PROMPT = """
Analiza el siguiente mensaje del usuario y extrae la siguiente información:

1) La postura del usuario (puede ser: 'a_favor', 'en_contra', 'neutral'). Si no se menciona una postura explícita, omite esta parte.
2) El tema principal del mensaje.
3) El tono del mensaje (puede ser: 'serio', 'sarcástico', 'informal', etc.).

Si no se identifica un tema principal, responde de forma graciosa pero respetuosa, y no incluyas ningún análisis de postura o tema.

Recuerda incluir siempre 'La postura del usuario' solo cuando se haya identificado una postura clara y un tema principal. Si no hay tema, simplemente responde de manera respetuosa y amigable.
"""

PROMPT_REFINACION = '''Refina esta respuesta para que sea mas natural'''
