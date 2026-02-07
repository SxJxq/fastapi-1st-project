#this file handles token creation and verification, making sure that the user that sent a request to my server is the same user that sent request to access anything
from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')#Defines how Fastapi exctracts the token, when someone logs in, they get tokens from /login

SECRET_KEY=settings.secret_key #signing the jwt
ALGORITHM=settings.algorithm#how the token is generated, encryption algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expire_minutes #token is valid 4 30 mins

#token from client to api, takes user info "id" and then returns a signed jwt token
def create_access_token(data: dict):# jwt payload must be a directory
    to_encode=data.copy()# data

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) #jwt contained exp field if i want it to expire automatically 

    #now the payload has a data(user_id) and exp

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM ) #converts payload to encrypted jwt string


def verify_access_token(token: str, credintials_exception):# decode token, validate it, extract user id
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])# verify segnature + expiration

        id: str = payload.get("user_id")

        if id is None:
            raise credintials_exception
        return schemas.TokenData(id=id)#warp id into a pydamtic model 4 validation
    
    
    except JWTError:
        raise credintials_exception
    

def get_current_user(token: str = Depends(oauth2_scheme)):
    credintials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate:": "Bearer"}
    )

    return verify_access_token(token, credintials_exception)#validate token & returns tokendata to the route handler
    


