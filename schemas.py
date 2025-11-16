# to sepetare the schema modles from the rest of the code
#PYDANTIC MODELS 
#pydanyic modles so we tell the frontend devs what to expect

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


#POST SCHEMAS
class PostBase(BaseModel):# common between req and res
    title: str
    content: str
    published: bool = True





class PostCreate(PostBase):#req input schema, if i wanted the user to send me some data but i dont want it to be returned to them
    pass 



class Post(PostBase):#res, fields r from the database, output schema
    id: int
    # created_at: datetime
    # owner_id: int 

    class Config:#transforming obj from sqlalchemy to json
        from_attributes = True
    

#USER SCHEMAS
#for input
class UserCreate(BaseModel):
    email: EmailStr
    password: str

#returned to the user
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:#transforming obj from sqlalchemy to json
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str 


#from api to login route
class Token(BaseModel):
    access_token:str
    token_type: str


#data extracted from the jwt (user id)
class TokenData(BaseModel):
    id: Optional[str] = None #it might return None



