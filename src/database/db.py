import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.const import DATABASE_URL
from src.database.models import Base

pymysql.install_as_MySQLdb()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
