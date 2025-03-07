from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.db import PROD_DATABASE_URL
from src.database.models import Menssagse


def get_chat_history(conversation_id: int):
    engine = create_engine(PROD_DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    db_conversation = session.query(Menssagse).filter(
        Menssagse.conversacion_id == conversation_id).limit(10).all()

    return db_conversation


def get_last_chat(conversation_id: int):
    engine = create_engine(PROD_DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    last_messages = session.query(Menssagse).filter(
        Menssagse.conversacion_id == conversation_id
    ).order_by(Menssagse.id.desc()).limit(5).all()

    return last_messages
