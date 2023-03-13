from fastapi import FastAPI,Body,HTTPException,Response,status,Depends,APIRouter
from ..database import engine,get_db
from .. import models,schemas,utils
from sqlalchemy import desc
from sqlalchemy.orm import Session
from random import randrange
from typing import List

router=APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Votes,db:Session=Depends(get_db),curr_user:int = Depends(utils.get_current_user)):
    
    posts=db.query(models.Posts).filter(vote.post_id==models.Posts.id).first()
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'vote with {vote.post_id} not found')
    
    vote_query=db.query(models.Votes).filter(
        vote.post_id==models.Votes.post_id,models.Votes.user_id==curr_user.id)
    
    found_vote=vote_query.first()
    
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user with user id {curr_user.id} has already voted')
        
        new_vote=models.Votes(post_id=vote.post_id,user_id=curr_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message":f"Succssfully voted with userid {curr_user.id}"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Vote doesnot exist')
        
        vote_query.delete()
        db.commit()
        
        return {"Message":f"Vote deleted Successfully from userid {curr_user.id}"}