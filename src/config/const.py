import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
# Configuración general del chatbot
BOT_NAME = "ChatBot"
DEFAULT_RESPONSE = "No entendí tu mensaje. ¿Puedes reformularlo?"
MAX_HISTORY_MESSAGES = 5