from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.db import PROD_DATABASE_URL
from src.database.models import Conversacion as dbConverssation
from src.database.models import Menssagse


def add_new_message(message, conversation_id, role):
    engine = create_engine(PROD_DATABASE_URL)
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

    print("datos agregaos")
    return None


def add_new_conversation(message: str) -> dict:
    engine = create_engine(PROD_DATABASE_URL)
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
