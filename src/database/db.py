import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base

pymysql.install_as_MySQLdb()
# SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER', 'root')}:{os.getenv('MYSQL_PASSWORD', 'pass123')}@localhost:3306/{os.getenv('MYSQL_DB', 'kopichallengedb')}"

# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:pass123@db:3306/kopichallengedb"
DATABASE_URL = 'mysql://vq87a2wc0jge3nyt:hidw10hcb40ds5km@nnmeqdrilkem9ked.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/kkjc39umeunk66pp'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
