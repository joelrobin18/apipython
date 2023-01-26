from sqlalchemy import Column,Integer,String,Boolean,Float
# from sqlalchemy.orm import *
from .database import Base

class Posts(Base):
    __tablename__ = "posts"
    
    id=Column(Integer ,nullable=False, primary_key=True)
    title=Column(String,nullable=False)
    caption=Column(String,nullable=False)
    author=Column(String,nullable=False)
    likes=Column(Integer, nullable=False,default=0)
    published=Column(Boolean, default=False,nullable=False)
    rating=Column(Float)