from fastapi import FastAPI
from database import engine
import models
from routers import posts, user, auth

#AUTO GENERATE TABLES
models.Base.metadata.create_all(bind=engine)

app = FastAPI()




app.include_router(posts.router)#to include routers
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "mew!"}
