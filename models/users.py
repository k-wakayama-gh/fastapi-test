# --- models/users.py ---

# modules
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# models below 000000000000000000000


# base model
class UserBase(SQLModel):
    username: str = Field(index=True)
    email: Optional[str] = Field(default=None)
    full_name: Optional[str] = Field(default=None)
    disabled: Optional[bool] = Field(default=False)


class UserInDB(UserBase):
    hashed_password: str



# table
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)



# create
class UserCreate(UserBase):
    pass



# read
class UserRead(UserBase):
    id: int



# update
class UserUpdate(UserBase):
    pass



# delete
class UserDelete(UserBase):
    pass

