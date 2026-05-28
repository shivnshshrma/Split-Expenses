from pydantic import BaseModel
from typing import Optional

class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None

class AddMember(BaseModel):
    username: str