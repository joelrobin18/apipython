from sqlalchemy import *
from .database import Base
class Posts(Base):
    __tablename__ = "posts"
    
    id=Column(Integer ,nullable=False, primary_key=True)
    title=Column(String,nullable=False)
    caption=Column(String,nullable=False)
    author=Column(String,nullable=False)
    likes=Column(Integer, nullable=False,server_default='0')
    created_at=Column(TIMESTAMP(timezone=true),nullable=False,server_default=text('NOW()'))
    published=Column(Boolean, server_default='False',nullable=False)
    rating=Column(Float)    


class User(Base):
    
    __tablename__ = 'users'
    id=Column(Integer,nullable=False,primary_key=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    username=Column(String,nullable=False,unique=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))
    firstname=Column(String,nullable=False)
    lastname=Column(String,nullable=False)
