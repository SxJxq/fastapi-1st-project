from fastapi import Response, status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, models, database
from typing import List
from database import get_db
import oauth2

router = APIRouter(
    prefix="/posts", #so we can replace /posts with just /
    tags=["Posts"] #organize docs
)




#GET ALL POSTS
@router.get("/", response_model=List[schemas.Post])#from api to user
def get_posts(db: Session=Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)): #DATA VALIDATION, from user to api, if the client provides a valid jwt, the route executes, otherwise a 401 error
    posts=db.query(models.Post).all()
    return posts




#CREATE ONE POST
@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session=Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):# data validation

    new_post=models.Post(**post.model_dump())#convert s sqlalchemy model into dictionary
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#GETTING ONE POST
@router.get("/{id}", response_model=schemas.Post)
def get_one_post(id: int, db: Session=Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} wasnt found")
    
    return post


#DELETING A POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} wasnt found")
    
    
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#UPDATING A POST
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session=Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    updated_post=db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} wasnt found")
    
    updated_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return updated_post.first()