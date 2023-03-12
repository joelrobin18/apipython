from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:%s@{settings.database_host_name}/{settings.database_name}'% quote_plus(f'{settings.database_password}')

# SQLALCHEMY_DATABASE_URL='postgresql://username:password@hostorip/database'
# print(SQLALCHEMY_DATABASE_URL)

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Depedency. To get or give a request to a database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()