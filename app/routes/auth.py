from fastapi import APIRouter,HTTPException,Depends,status
from fastapi.security import OAuth2PasswordRequestForm
from .. import utils,schemas,database,models
from sqlalchemy.orm import Session

router=APIRouter(
    prefix='/login',
    tags=['Authentication']
)

@router.post("/",status_code=status.HTTP_202_ACCEPTED)
def login(user_cred:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(database.get_db)):
    
    # print(user_cred.username,user_cred.password,user_cred.client_id)
    
    user = db.query(models.User).filter(models.User.email==user_cred.username).first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    verified = utils.verify_user(user_cred.password, user.password)
    
    if not verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    data = {
        "user_id":user.id
    }
    
    jwt_token = utils.create_access_token(data)
    
    return {"message":"Authentication Successfull",
            "JWT_Token": jwt_token,
            "Token Type":"bearer"}