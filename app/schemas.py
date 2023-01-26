from pydantic import BaseModel
from typing import Optional
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

class ResponsePost(Update):
    likes:int
    
    class Config:
        orm_mode=True
