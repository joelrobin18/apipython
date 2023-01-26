from fastapi import FastAPI,Body,HTTPException,Response,status,Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange
from app.data import *
import psycopg2 as db
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine
import time ## Timer for sleep for or wait for certain amount of time
app=FastAPI()

models.Base.metadata.create_all(bind=engine)

# Depedency. To get or give a request to a database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# try:
#     conn=db.connect(host="blaaaa",
#                             database="blaaaaa", 
#                             user="blaaaa",
#                             password="1234567890")
    
#     cursor=conn.cursor()
#     print("Database Successfully Connected")
# except Exception as error:
#     print("Error",error)
#     pass

## Schema Validation
class Post(BaseModel):
    title:str
    caption:str
    author:str
    published:bool = False
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
    cursor.execute("""select * from post """)
    posts = cursor.fetchall()
    return {"Post":posts}


# Creating a new post
@app.post("/posts",status_code=status.HTTP_201_CREATED) ## Status Code Changed for creating a new post
def create(Post:Post):
    # post=post.dict()
    # post['id']=randrange(0,10000)
    # posts.append(post)
    cursor.execute("""INSERT INTO post (title,caption,author,rating) VALUES (%s,%s,%s,%s) RETURNING *""",(Post.title,Post.caption,Post.author,Post.rating))
    posts=cursor.fetchone()
    conn.commit()
    
    cursor.execute("""SELECT * from post""")
    all_posts=cursor.fetchall()
    
    return {"New Post":posts,
            "All Post":all_posts}


# Get the latest Post
@app.get("/posts/latest")
def latest():
    # latest_posts=[]
    # latest_posts.append(posts[len(posts)-1])
    # latest_posts.append(posts[len(posts)-2])
    cursor.execute("""SELECT * from post ORDER BY time desc LIMIT 3 """)
    latest_posts=cursor.fetchall()
    return {"Latest Post":latest_posts}


# Getting a particular post 
@app.get("/posts/{id}")
def get_post(id:int):
    # post= find_post(id) 
    cursor.execute("""SELECT * from post where id = %s""",(str(id),))
    post=cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"The post with id : {id} is not found")
    
    return {"message":post}

#Delete all the post
@app.delete("/posts/delete/all",status_code=status.HTTP_204_NO_CONTENT)
def delete_all_post():
    # posts.clear()
    cursor.execute("""DELETE from post returning *""")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) # While deleting a content we dont need to return any response. So we return no content as response


#Delete a post with particular id
@app.delete("/posts/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    # i=-1
    # deletepost,index=find_post_index(id,i)
    # if index==-1:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                     detail=f"The post with id : {id} is not found")
    
    cursor.execute("""DELETE from post where id=%s RETURNING *""",(str(id),))
    deleted_post=cursor.fetchone()
    
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the id: {id} is not found")
    
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


## Updating a post as completely
@app.put("/posts/{id}")
def update(id:int,post:Post):
    i=-1
    post_value,index=find_post_index(id,i)
    
    
    ## Using database
    cursor.execute("""UPDATE post set title=%s ,caption=%s ,author=%s  where id = %s  RETURNING *""",(post.title,post.caption,post.author,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    
    if  updated_post== None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id {id} not found")

    # updated_post=post.dict() # Convert the class into dict
    # updated_post['id']=id # Store the data with the same id
    # posts[index]=updated_post # Store the same data into the same index
    
    return {"Post Updated":updated_post}