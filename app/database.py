from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus


# SQLALCHEMY_DATABASE_URL='postgresql://username:password@hostorip/database'

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