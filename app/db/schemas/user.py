from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str
    is_active: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
