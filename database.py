from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
import os




#DATABASE URL
SQLALCHEMY_DATABASE_URL = (f"postgresql://{os.getenv('DATABASE_USERNAME')}:" f"{os.getenv('DATABASE_PASSWORD')}@" f"{os.getenv('DATABASE_HOSTNAME')}:" f"{os.getenv('DATABASE_PORT')}/" f"{os.getenv('DATABASE_NAME')}")


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
