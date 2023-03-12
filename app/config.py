from pydantic import BaseSettings

class Settings(BaseSettings):
    database_username:str
    database_password:str
    database_host_name:str
    database_name:str
    secret_key:str
    algorithm:str
    access_token_expire_time:int
    
    class Config:
        env_file=".env"

settings = Settings()