from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Conversacion(Base):
    __tablename__ = "conversaciones"  # Nombre de la tabla en tu BD
    conversation_id = Column(Integer, primary_key=True, index=True)
    message = Column(Integer, nullable=False)
    fecha_inicio = Column(DateTime, default=datetime.utcnow)


