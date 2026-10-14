from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    SUPA_URL: str = ""
    SUPA_ANON_KEY:str = ""
    SUPA_SERVICE_KEY:str = ""
    SUPA_SCHEMA:str = ""
    
    class Config:
        env_file = os.getenv("FASTAPI_ENV", "dev") + '.env'
        env_file_encoding = 'utf-8'
        
settings = Settings()