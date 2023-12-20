# --- route_html.py ---

# modules
from fastapi import FastAPI, APIRouter, Request, Header, Body, HTTPException, Depends, Query, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, select
from typing import Optional, List, Annotated

# my modules
from database import engine, get_session
from models.items import Item, ItemCreate, ItemRead, ItemUpdate, ItemDelete
from models.users import User, UserCreate, UserRead, UserUpdate, UserDelete
from models.todos import Todo, TodoCreate, TodoRead, TodoUpdate, TodoDelete

# FastAPI instance and API router
app = FastAPI()
router = APIRouter()

# templates settings
templates = Jinja2Templates(directory='templates')

# routes below 000000000000000000000000000000000000


# top page
@router.get("/", response_class=HTMLResponse, tags=["html"])
def index(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("index.html", context)



# coffee page
@router.get("/coffee", response_class=HTMLResponse, tags=["html"])
def coffee(request: Request):
    context = {
        'request': request,
    }
    return templates.TemplateResponse('coffee.html', context)



from route_todos import read_todos_list

# display todos
@router.get("/todos", response_class=HTMLResponse, tags=["html"])
def display_todos(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100), request: Request):
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    if not todos:
        raise HTTPException(status_code=404, detail="Not found")
    context = {
        "request": request,
        "todos": todos,
    }
    return templates.TemplateResponse("todos.html", context)
