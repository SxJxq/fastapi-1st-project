# to sepetare the schema modles from the rest of the code
#PYDANTIC MODELS 
#pydanyic modles so we tell the frontend devs what to expect
from pydantic import BaseModel
import datetime



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
    


