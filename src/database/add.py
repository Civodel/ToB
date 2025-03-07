import logging
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from src.config.const import DATABASE_URL
from src.database.models import Conversacion as dbConverssation
from src.database.models import Menssagse


def add_new_message(message, conversation_id, role):
    try:
        # Crear la conexión y la sesión
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()

        new_message = Menssagse(
            conversacion_id=conversation_id,
            usuario=role,
            mensaje=message,
            fecha_envio=datetime.utcnow())

        session.add(new_message)
        session.commit()
        session.refresh(new_message)

        return None

    except SQLAlchemyError as e:

        logging.error(f"Error al agregar el mensaje: {e}")
        session.rollback()
        return {"error": str(e)}

    finally:

        session.close()


def add_new_conversation(message: str) -> dict:
    try:

        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()

        new_conversation = dbConverssation(
            message=message,
            fecha_inicio=datetime.utcnow())

        session.add(new_conversation)
        session.commit()
        session.refresh(new_conversation)

        conversacion_dict = {k: v for k, v in vars(new_conversation).items() if k != "_sa_instance_state"}

        return conversacion_dict

    except SQLAlchemyError as e:

        logging.error(f"Error al agregar la conversación: {e}")
        session.rollback()
        return {"error": str(e)}

    finally:

        session.close()
