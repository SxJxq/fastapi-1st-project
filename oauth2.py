#this file handles token creation and verification, making sure that the user that sent a request to my server is the same user that sent request to access anything
from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_schema=OAuth2PasswordBearer(tokenUrl='login')#Defines how Fastapi exctracts the token, when someone logs in, they get tokens from /login

SECRET_KEY="solasala558" #signing the jwt
ALGORITHM="HS256"#how the token is generated, encryption algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30 #token is valid 4 30 mins


#token from client to api
def create_access_token(data: dict):
    to_encode=data.copy()# data

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) #jwt contained exp field if i want it to expire automatically 

    #now the payload has a data(user_id) and exp

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM )


def verify_access_token(token: str, credintials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM] )

        id: str = payload.get("user_id")

        if id in None:
            raise credintials_exception
        return schemas.TokenData(id=id)#warp id into a pydamtic model
    
    
    except JWTError:
        raise credintials_exception
    

def get_current_user(token: str = Depends(oauth2_schema)):
    credintials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate:": "Bearer"}
    )

    return verify_access_token(token, credintials_exception)#validate token & returns tokendata to the route handler
    


