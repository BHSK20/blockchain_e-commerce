from pydantic_settings import BaseSettings
import typing

class Config(BaseSettings):
    class Config:
        env_file = ".env"
    AD_PUBLIC_KEY: str
    AD_PRIVATE_KEY: str
    CHAIN_ID: int
    SECRET_KEY: str
    PROJECT_NAME: str = 'blockchain-e-commerce'
    POSTGRES_URI: str
    REDIS_URL: str
    INFURA_API_KEY: str
    PORT: typing.Optional[int]
    # BROKER_URL: str
    CELERY_ROUTES: dict = {
        'worker.send_mail': {'queue': 'send_mail'},
    }
    CELERY_IMPORTS: list = ['src.tasks']
    CELERY_RESULT_BACKEND:str = 'rpc://'
    CELERY_TRACK_STARTED:bool = True
    CELERY_RESULT_PERSISTENT:bool = True
    KEY_JWT: str
    ALGORITHM_HASH_TOKEN: str = "HS256"
    BASE_URL_TOKEN: str
config = Config()