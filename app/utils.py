from fastapi import Depends,HTTPException,status
from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas
from .config import settings
from fastapi.security import OAuth2PasswordBearer
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth=OAuth2PasswordBearer(tokenUrl="login")

def hash(password:str):
    return pwd_content.hash(password)

def verify_user(given_password,hashed_password):
    return pwd_content.verify(given_password,hashed_password)


# JWT Token Creation

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_time

def create_access_token(data:dict):
    encode=data.copy()
    
    expire=datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp":expire})
    JWT_TOKEN=jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return JWT_TOKEN

def verify_jwt(token:str, credentials_exception):
    try:
        
        decode=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id:str = decode.get("user_id")
        
        if id == None:
            raise credentials_exception
        
        jwt_data=schemas.TokenData(id=id)
        
    except JWTError:
        raise credentials_exception
    
    return jwt_data

def get_current_user(token:str =  Depends(oauth)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail=f"Not Authorized")
    
    return verify_jwt(token, credentials_exception)
