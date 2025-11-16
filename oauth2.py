#this file handles token creation and verification, making sure that the user that sent a request to my server is the same user that sent request to access anything
from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas

SECRET_KEY="solasala558" #signing the jwt
ALGORITHM="HS256"#how the token is generated
ACCESS_TOKEN_EXPIRE_MINUTES=30 #token is valid 4 30 mins


#token to access protected routs
def create_access_token(data: dict):
    to_encode=data.copy()

    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM )


def verify_access_token(token: str, credintials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM] )

        id: str = payload.get("user_id")

        if id in None:
            raise credintials_exception
        return schemas.TokenData(id=id)
    
    
    except JWTError:
        raise credintials_exception
