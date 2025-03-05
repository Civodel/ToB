from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import create_engine

from sqlalchemy.orm import Session, sessionmaker
from src.database.db import get_db, SQLALCHEMY_DATABASE_URL
from src.database.models import Conversacion as dbConverssation

from src.database.models import Menssagse



def add_new_message(message):

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    new_message=Menssagse(
        conversacion_id=1,
        usuario="user",
        mensaje=message,
        fecha_envio=datetime.utcnow())
    session.add(new_message)
    session.commit()
    session.refresh(new_message)



    print("datos agregaos")
    return None









