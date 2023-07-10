from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

from ugeougeo.config import env

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{env.DB_ID}:{env.DB_PASSWORD}@{env.DB_URL}/ugeougeo"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
