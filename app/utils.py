from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    return pwd_content.hash(password)

def verify_user(given_password,hashed_password):
    return pwd_content.verify(given_password,hashed_password)


# JWT Token Creation

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    encode=data.copy()
    
    expire=datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp":expire})
    JWT_TOKEN=jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return JWT_TOKEN
