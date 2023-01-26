from fastapi import FastAPI,Body,HTTPException,Response,status,Depends
from random import randrange
from typing import List
import psycopg2 as dbs
from sqlalchemy import desc
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine,get_db
import time ## Timer for sleep for or wait for certain amount of time
app=FastAPI()

models.Base.metadata.create_all(bind=engine)

## To make get request to the server. To get the data
@app.get("/posts",response_model=List[schemas.ResponsePost]) 
def root(db:Session=Depends(get_db)):
    
    # Using Raw SQL
    # cursor.execute("""select * from post """)
    # posts = cursor.fetchall()
    
    # Using SQLALCHEMY or ORM
    posts =db.query(models.Posts).all()
    return posts


# Creating a new post
@app.post("/posts",status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost) ## Status Code Changed for creating a new post
def create(post:schemas.PostCreate,db:Session=Depends(get_db)):
    
    # Using pure python without database
    # post=post.dict()
    # post['id']=randrange(0,10000)
    # posts.append(post)
    
    # Using Raw SQL as database
    # cursor.execute("""INSERT INTO post (title,caption,author,rating) VALUES (%s,%s,%s,%s) RETURNING *""",(Post.title,Post.caption,Post.author,Post.rating))
    # posts=cursor.fetchone()
    # conn.commit()
    # cursor.execute("""SELECT * from post""")
    # all_posts=cursor.fetchall()
    
    # Using SQLALCHEMY or ORM
    new_post=models.Posts(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


# Get the latest Post
@app.get("/posts/latest",response_model=List[schemas.ResponsePost])
def latest(db:Session=Depends(get_db)):
    
    # Using pure python without db
    # latest_posts=[]
    # latest_posts.append(posts[len(posts)-1])
    # latest_posts.append(posts[len(posts)-2])
    
    # Using Raw SQL with python
    # cursor.execute("""SELECT * from post ORDER BY time desc LIMIT 3 """)
    # latest_posts=cursor.fetchall()
    
    # Using SQLALCHEMY or ORM
    latest_posts=db.query(models.Posts).order_by(desc(models.Posts.created_at)).limit(2).all()
    # print(latest_posts)
    return latest_posts


# Getting a particular post 
@app.get("/posts/{id}",response_model=schemas.ResponsePost)
def get_post(id:int,db:Session=Depends(get_db)):
    # post= find_post(id) 
    # cursor.execute("""SELECT * from post where id = %s""",(str(id),))
    # post=cursor.fetchone()
    
    ## Getting a particular post using ORM
    post =db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"The post with id : {id} is not found")
    
    return post

#Delete all the post
@app.delete("/posts/delete/all",status_code=status.HTTP_204_NO_CONTENT)
def delete_all_post(db:Session=Depends(get_db)):
    # posts.clear()
    # cursor.execute("""DELETE from post returning *""")
    # conn.commit()
    
    # Delete all post using ORM
    db.query(models.Posts).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) # While deleting a content we dont need to return any response. So we return no content as response


#Delete a post with particular id
@app.delete("/posts/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    # i=-1
    # deletepost,index=find_post_index(id,i)
    # if index==-1:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                     detail=f"The post with id : {id} is not found")
    
    # cursor.execute("""DELETE from post where id=%s RETURNING *""",(str(id),))
    # deleted_post=cursor.fetchone()
    
    deleted_post=db.query(models.Posts).filter(models.Posts.id==id).first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the id: {id} is not found")
    
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


## Updating a post as completely
@app.put("/posts/{id}",response_model=schemas.ResponsePost)
def update(id:int,post:schemas.Update,db:Session=Depends(get_db)):
    # i=-1
    # post_value,index=find_post_index(id,i)
    
    
    ## Using database Raw SQL and Python
    # cursor.execute("""UPDATE post set title=%s ,caption=%s ,author=%s  where id = %s  RETURNING *""",(post.title,post.caption,post.author,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    # updated_post=post.dict() # Convert the class into dict
    # updated_post['id']=id # Store the data with the same id
    # posts[index]=updated_post # Store the same data into the same index
    
    
    # Using ORM and python
    updated_post=db.query(models.Posts).filter(models.Posts.id==id)
    if  updated_post== None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id {id} not found")
    
    updated_post.update(post.dict())
    db.commit()
    
    return updated_post.first()

