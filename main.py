from fastapi import FastAPI,Body,HTTPException,Response,status
from pydantic import BaseModel
from typing import Optional
from random import randrange
from data import *
app=FastAPI()

## Schema Validation
class Post(BaseModel):
    title:str
    caption:str
    author:str
    rating:Optional[float]=None


# Function for finding the post with particular id
def find_post(id):
    for i in posts:
        if i['id']==id:
            return i

def find_post_index(id,i):
    for post in posts:
        i=i+1
        if post['id']==id:
            return (post,i)
    
    return (None,-1)
## To make get request to the server. To get the data
@app.get("/posts") 
def root():
    return {"Post":posts}


# Creating a new post
@app.post("/posts",status_code=status.HTTP_201_CREATED) ## Status Code Changed for creating a new post
def create(post:Post):
    post=post.dict()
    post['id']=randrange(0,10000)
    posts.append(post)
    return {"All Post":posts}


# Get the latest Post
@app.get("/posts/latest")
def latest():
    latest_posts=[]
    latest_posts.append(posts[len(posts)-1])
    latest_posts.append(posts[len(posts)-2])
    return {"Latest Post":latest_posts}


# Getting a particular post 
@app.get("/posts/{id}")
def get_post(id:int):
    post= find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"The post with id : {id} is not found")
    
    return {"message":post}

#Delete all the post
@app.delete("/posts/delete/all")
def delete_all_post():
    posts.clear()
    return {"Message":"Post Deleted Successfully",
            "Posts":posts}


#Delete a post with particular id
@app.delete("/posts/delete/{id}")
def delete_post(id:int):
    i=-1
    deletepost,index=find_post_index(id,i)
    if index==-1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"The post with id : {id} is not found")
    
    posts.pop(index)
    return {"Message":"Post Deleted Successfully",
            "Post":posts}
    
    

