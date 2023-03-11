from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime
## Schema Validation
class Post(BaseModel):
    title:str
    caption:str
    author:str
    published:bool = False
    rating:Optional[float]=None

class PostCreate(Post):
    pass

class Update(Post):
    published:bool
    rating:float
    
class UserResponse(BaseModel):
    email:EmailStr
    username:str
    firstname:str
    lastname:str
    
    class Config:
        orm_mode=True        

class ResponsePost(Update):
    likes:int
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