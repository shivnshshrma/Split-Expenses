from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from pydantic import BaseModel

# Absolute imports
# from data.users import user_db
from models.User import User

load_dotenv()
SECRET_KEY = os.getenv("JWT_TOKEN")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData(BaseModel):
    username: str | None = None

# create jwt token
def create_access_session(data: dict):
    to_encode = data.copy()
    expire = datetime() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    create_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise create_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise create_exception

    user = user_db.get(token_data.username)
    if user is None:
        raise create_exception
    return user


    