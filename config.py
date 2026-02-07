from pydantic import BaseSettings #reads environment variables and validates them


class Settings(BaseSettings):#defining what conf my app requires
    #in one is missing from .env, the app wont start
    database_hostname: str
    database_port:str
    database_password: str
    database_name: str
    database_username: str

    #jwt settings
    secret_key: str
    algorithm:str
    access_token_exp_minutes: int



    #automatically load .env, we wont need os.getenv()
    class Config:
        env_file = ".env"

    settings=Settings() #reads .env, validates everything, stores config in one object

