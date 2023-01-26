from sqlalchemy import *
# from sqlalchemy.orm import *
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
