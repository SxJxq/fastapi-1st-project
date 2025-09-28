from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:7364@localhost/postgres"

#TO CONNECT TO POSTGRES
engine = create_engine(SQLALCHEMY_DATABASE_URL)


#CREATES DB SESSIONS 4 QUERIES
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#BASE CLASS FOR ALL ORM MODLES
Base=declarative_base()