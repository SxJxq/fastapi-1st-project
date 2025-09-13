from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

#PYDANTIC MODELS 
#pydanyic modles so we tell the frontend devs what to expect


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

#POST ROOT
@app.post("/posts")
def posts(post: Post): #DATA VALIDATION
    return{"data":post}



@app.get("/")
def root():
    return {"message": "mew!"}

