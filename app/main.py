from fastapi import FastAPI
from . import models
from .routes import user,post,auth
from .database import engine,get_db
import time ## Timer for sleep for or wait for certain amount of time
app=FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return "Welcome to our API"