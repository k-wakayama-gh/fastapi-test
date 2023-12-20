# --- route_auth.py ---

# modules
from fastapi import FastAPI, APIRouter, Request, Header, Body, HTTPException, Depends, Query, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Session, select
from typing import Optional, List, Annotated

# my modules
from database import engine, get_session
from models.auth import Auth, AuthCreate, AuthRead, AuthUpdate, AuthDelete
from models.users import User, UserCreate, UserRead, UserUpdate, UserDelete, UserInDB

# FastAPI instance and API router
app = FastAPI()
router = APIRouter()

# templates settings
templates = Jinja2Templates(directory='templates')

# auth scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# routes below 000000000000000000000000000000000000

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


def fake_hash_password(password: str):
    return "fakehashed" + password



def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user





def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            # status_code=status.HTTP_401_UNAUTHORIZED,
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user



# 00000000000000000


# create
@router.post("/auth", response_model = AuthRead, tags=["Auth"])
def create_auth(*, session: Session = Depends(get_session), auth: AuthCreate):
    db_auth = Auth.from_orm(auth)
    session.add(db_auth)
    session.commit()
    session.refresh(db_auth)
    return db_auth



# read list
@router.get("/auth", tags=["Auth"])
async def read_auth(token: Annotated[str, Depends(oauth2_scheme)]): # non-annotated: read_auth(token: str = Depends(oauth2_scheme))
    return {"token": token}




# read one
@router.get("/auth/{auth_id}", response_model = AuthRead, tags=["Auth"])
def read_auth(*, session: Session = Depends(get_session), auth_id: int):
    auth = session.get(Auth, auth_id)
    if not auth:
        raise HTTPException(status_code=404, detail="Not found")
    return auth



# update
@router.patch("/auth/{auth_id}", response_model = AuthRead, tags=["Auth"])
def update_auth(*, session: Session = Depends(get_session), auth_id: int, auth: AuthUpdate):
    db_auth = session.get(Auth, auth_id)
    if not db_auth:
        raise HTTPException(status_code=404, detail="Not found")
    auth_data = auth.model_dump(exclude_unset=True)
    for key, value in auth_data.auth():
        setattr(db_auth, key, value)
    session.add(db_auth)
    session.commit()
    session.refresh(db_auth)
    return db_auth



# delete
@router.delete("/auth/{auth_id}", tags=["Auth"])
def delete_auth(*, session: Session = Depends(get_session), auth_id: int):
    auth = session.get(Auth, auth_id)
    if not auth:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(auth)
    session.commit()
    return {"ok": True}


