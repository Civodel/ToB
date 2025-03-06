from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Conversacion(Base):
    __tablename__ = "conversaciones"
    conversation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message = Column(Text, nullable=False)
    fecha_inicio = Column(DateTime, default=datetime.utcnow)


class Menssagse(Base):
    __tablename__ = "mensajes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    conversacion_id = Column(Integer, )
    usuario = Column(String(255), nullable=False)
    mensaje = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, default=datetime.utcnow)
