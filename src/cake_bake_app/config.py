from pydantic import BaseSettings

class Settings(BaseSettings):

    db_name:str
    api_port:int
    api_host:str
    api_worker_count:int = 4

    class Config:
            env_file = '.env'
            env_file_encoding = 'utf-8'

config = Settings()