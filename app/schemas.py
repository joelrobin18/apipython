from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint
## Schema Validation
class Post(BaseModel):
    id:int
    title:str
    caption:str
    author:str
    published:bool = False
    rating:Optional[float]=None

class PostCreate(BaseModel):
    title:str
    caption:str
    author:str
    published:bool = False
    rating:Optional[float]=None

class Update(Post):
    published:bool
    rating:float
    
class UserResponse(BaseModel):
    id:str
    email:EmailStr
    username:str
    firstname:str
    lastname:str
    
    class Config:
        orm_mode=True        

class ResponsePost(Update):
    created_at:datetime
    user_id:int
    user:UserResponse
    class Config:
        orm_mode=True

class User(BaseModel):
    email:EmailStr
    password:str
    username:str
    firstname:str
    lastname:str


class UserUpdate(BaseModel):
    email:EmailStr
    username:str
    firstname:str
    lastname:str

class UserCredentials(BaseModel):
    email:EmailStr
    password:str

class TokenData(BaseModel):
    id:Optional[int]= None

class Votes(BaseModel):
    post_id:int
    dir:conint(le=1)    

class PostLike(BaseModel):
    Posts: ResponsePost
    Likes: int
    class Config:
        orm_mode=True