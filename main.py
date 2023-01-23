from fastapi import FastAPI,Body,HTTPException,Response,status
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

## Saving your data/ Database is not included now
## On refreshing the data get changed. So its not stored permenantly
posts=[ {
            "title": "Test Post 1",
            "caption": "Test Caption 1",
            "author": "Test 1",
            "rating": 4.2,
            "id": 1
        },
        {
            "title": "Test Post 2",
            "caption": "Test Caption 2",
            "author": "Test 3",
            "rating": 5.6,
            "id": 2
        },
        {
            "title": "Test Post 3",
            "caption": "Test Caption 2",
            "author": "Test 3",
            "rating": 10.0,
            "id": 3
        }]

## To make get request to the server. To get the data
@app.get("/posts") 
def root():
    return {"Post":posts[2]['title']}

@app.post("/posts",status_code=status.HTTP_201_CREATED) ## Status Code Changed for creating a new post
def create(post:Post):
    post=post.dict()
    post['id']=randrange(0,10000)
    posts.append(post)
    return {"All Post":posts}
