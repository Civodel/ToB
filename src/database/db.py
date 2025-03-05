from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from src.config.const import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER', 'root')}:{os.getenv('MYSQL_PASSWORD', 'pass123')}@localhost:3306/{os.getenv('MYSQL_DB', 'kopichallengedb')}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
#f"mysql+mysqlconnector://{os.getenv('MYSQL_USER', 'root')}:{os.getenv('MYSQL_PASSWORD', 'pass123')}@{os.getenv('MYSQL_HOST', 'db')}/{os.getenv('MYSQL_DB', 'kopichallengedb')}"
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


