from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
import schemas, models
from psycopg2.extras import RealDictCursor
from typing import List
from database import engine, SessionLocal


#AUTO GENERATE TABLES
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#DEPENDENCY TO GET DB SESSION
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.get("/")
def root():
    return {"message": "mew!"}

#GET ALL POSTS
@app.get("/posts", response_model=List[schemas.Post])#from api to user
def get_posts(db: Session=Depends(get_db)): #DATA VALIDATION, from user to api
    posts=db.query(models.Post).all()
    return posts




#CREATE ONE POST
@app.post("/posts", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session=Depends(get_db)):# data validation

    new_post=models.Post(**post.model_dump())#convert s pydantic model into dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#GETTING ONE POST
@app.get("/posts/{id}", response_model=schemas.Post)
def get_one_post(id: int, db: Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} wasnt found")
    
    return post


#DELETING A POST
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} wasnt found")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#UPDATING A POST
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session=Depends(get_db)):
    updated_post=db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} wasnt found")
    
    updated_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return updated_post.first()


