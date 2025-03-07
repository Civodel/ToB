from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.db import SQLALCHEMY_DATABASE_URL
from src.database.models import Menssagse


def get_chat_history(conversation_id):
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    db_conversation = session.query(Menssagse).filter(
        Menssagse.conversacion_id == conversation_id).all()

    return db_conversation


def get_last_chat(conversation_id):
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    last_messages = session.query(Menssagse).filter(
        Menssagse.conversacion_id == conversation_id
    ).order_by(Menssagse.id.desc()).limit(5).all()

    return last_messages
