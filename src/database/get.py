import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from src.config.const import DATABASE_URL
from src.database.models import Menssagse


# Crear una sesión de base de datos
def get_db_session():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


# Obtener el historial de un chat
def get_chat_history(conversation_id: int):
    try:
        session = get_db_session()
        db_conversation = session.query(Menssagse).filter(
            Menssagse.conversacion_id == conversation_id
        ).limit(15).all()
        return db_conversation if db_conversation else []  # Retorna una lista vacía si no hay resultados
    except SQLAlchemyError as e:
        logging.error(f"Error al obtener el historial de chat para el ID: {conversation_id}: {e}")
        return []  # Retorna una lista vacía en caso de error
    finally:
        session.close()


# Obtener los últimos mensajes de un chat
def get_last_chat(conversation_id: int):
    try:
        session = get_db_session()
        last_messages = session.query(Menssagse).filter(
            Menssagse.conversacion_id == conversation_id
        ).order_by(Menssagse.id.desc()).limit(10).all()
        return last_messages if last_messages else []  # Retorna una lista vacía si no hay resultados
    except SQLAlchemyError as e:
        logging.error(f"Error al obtener los últimos mensajes del chat para el ID: {conversation_id}: {e}")
        return []  # Retorna una lista vacía en caso de error
    finally:
        session.close()
