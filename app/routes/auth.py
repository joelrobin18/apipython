from fastapi import APIRouter,HTTPException,Depends,status
from .. import utils,schemas,database,models
from sqlalchemy.orm import Session

router=APIRouter(
    prefix='/login',
    tags=['Authentication']
)

@router.post("/",status_code=status.HTTP_202_ACCEPTED)
def login(user_cred:schemas.UserCredentials,db:Session=Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email==user_cred.email).first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    
    verified = utils.verify_user(user_cred.password, user.password)
    
    if not verified:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")

    return {"message":"Authentication Successfull"}