#Models are the stucture for different parts of application

# This is a user model which defines the structure of user data.

# More info: This is a pydantic model which is used to validate data 
# stay alive for few seconds (small time).

from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    name: str
    email: str
    password: str
    phone_number: str 

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None