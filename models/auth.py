# --- models/auth.py ---

# modules
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# models below 000000000000000000000


# base model
class AuthBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] =Field(default=None, index=True)




# table
class Auth(AuthBase):
    id: Optional[int] = Field(default=None, primary_key=True)



# create
class AuthCreate(AuthBase):
    pass



# read
class AuthRead(AuthBase):
    id: int



# update
class AuthUpdate(AuthBase):
    pass



# delete
class AuthDelete(AuthBase):
    pass


