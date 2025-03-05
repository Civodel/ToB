from fastapi import APIRouter, Depends
from sqlalchemy import create_engine

from sqlalchemy.orm import Session, sessionmaker
from src.database.db import get_db, SQLALCHEMY_DATABASE_URL
from src.database.models import Conversacion as dbConverssation



def get_chat_history(conversation_id, ):
    print("todo pantera")
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    db_conversation = session.query(dbConverssation).filter(
        dbConverssation.conversation_id == conversation_id).first()

    print("Busqueda perronas")
    return db_conversation







