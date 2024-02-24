from pydantic_settings import BaseSettings
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

class Setting(BaseSettings):
    database_hostname :str
    database_port :str
    database_password :str
    database_name :str
    database_username:str
    secret_key:str
    algorithm :str
    access_token_expire_minutes:int
        
    class Config():
        env_file=".env"

  
        
settings = Setting()
