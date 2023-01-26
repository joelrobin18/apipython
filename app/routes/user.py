from fastapi import FastAPI,Body,HTTPException,Response,status,Depends,APIRouter
from ..database import engine,get_db
from .. import models,schemas,utils
from sqlalchemy import desc
from sqlalchemy.orm import Session
from random import randrange
from typing import List


router=APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.get("/",response_model=List[schemas.UserResponse])
def userdetails(db:Session=Depends(get_db)):
    all_users=db.query(models.User).all()
    return all_users


@router.get("/latest",response_model=List[schemas.UserResponse])
def latestUser(db:Session=Depends(get_db)):
    latest_users=db.query(models.User).order_by(desc(models.User.created_at)).limit(2).all()
    return latest_users


@router.get("/{id}",response_model=schemas.UserResponse)
def userwithid(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} does not exist")
    return user


@router.post("/create",response_model=schemas.UserResponse,status_code=status.HTTP_201_CREATED)
def createUser(user:schemas.User,db:Session=Depends(get_db)):
    
    pwd=utils.hash(user.password)
    user.password = pwd
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_a_user(id:int,db:Session=Depends(get_db)):
    deleted_user=db.query(models.User).filter(models.User.id==id).first()
    
    if deleted_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} does not exist")
    
    db.delete(deleted_user)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/update/{id}",response_model=schemas.UserResponse)
def update_user(id:int,update:schemas.UserUpdate,db:Session=Depends(get_db)):
    
    update_user=db.query(models.User).filter(models.User.id==id)
    if update_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} does not exist")
    
    update_user.update(update.dict())
    db.commit()
    
    return update_user.first()