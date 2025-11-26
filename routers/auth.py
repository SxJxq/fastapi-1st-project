#authentication/login router
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from utils import verify
from oauth2 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):

    #find user with same email
    user=db.query(models.User).filter(models.User.email == user_cred.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credinteals")

    #verify password connected to the user:
    if not verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credinteals")
    
    access_token = create_access_token(data={"user_id" : user.id})#puts the user id into the payload
    
    return {"access_token": access_token, "token_type": "bearer"}
