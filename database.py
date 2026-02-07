from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from config import settings 



#DATABASE URL
SQLALCHEMY_DATABASE_URL = (f"postgresql://{settings.database_username}:" f"{settings.database_password}@" f"{settings.database_hostname}:" f"{settings.database_port}/" f"{settings.database_name}")


print("DATABASE URL:", SQLALCHEMY_DATABASE_URL)


#TO CONNECT TO POSTGRES
engine = create_engine(SQLALCHEMY_DATABASE_URL)


#CREATES DB SESSIONS 4 QUERIES
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#BASE CLASS FOR ALL ORM MODLES
Base=declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
