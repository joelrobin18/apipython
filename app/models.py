from sqlalchemy import *
from sqlalchemy.orm import relationship
from .database import Base
# Model contain all our table which we needed in our backend app
class Posts(Base):
    __tablename__ = "post"
    
    id=Column(Integer ,nullable=False, primary_key=True)
    title=Column(String,nullable=False)
    caption=Column(String,nullable=False)
    author=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=true),nullable=False,server_default=text('NOW()'))
    published=Column(Boolean, server_default='False',nullable=False)
    rating=Column(Float)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    user = relationship("User")   # Update the responce model


class User(Base):
    
    __tablename__ = 'users'
    id=Column(Integer,nullable=False,primary_key=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    username=Column(String,nullable=False,unique=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))
    firstname=Column(String,nullable=False)
    lastname=Column(String,nullable=False)
    
class Votes(Base):

    __tablename__ = "votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id",ondelete="CASCADE"),primary_key=True)
