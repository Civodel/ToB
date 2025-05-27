import time

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from src.config.const import DATABASE_URL
from src.database.models import Base

pymysql.install_as_MySQLdb()

MAX_RETRIES = 10
RETRY_DELAY = 2

# Intenta conectar con reintentos
for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Conectado a la base de datos y tablas creadas (si no existían)")
        break
    except OperationalError as e:
        print(f"❌ Error de conexión a MySQL (intento {attempt + 1}/{MAX_RETRIES}): {e}")
        time.sleep(RETRY_DELAY)
else:
    raise RuntimeError("⛔ No se pudo conectar a la base de datos después de varios intentos.")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
