from fastapi import FastAPI,Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app=FastAPI()

## Schema Validation
class Post(BaseModel):
    title:str
    caption:str
    author:str
    rating:Optional[float]=None

## To make get request to the server. To get the data
@app.get("/posts") 
def root():
    return {"message":"Hello World"}

@app.post("/posts")
def create(post:Post):
    post=post.dict()
    post['id']=randrange(0,10000)
    return {"message":post}
