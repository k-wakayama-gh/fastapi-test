# --- route_todos.py ---

# modules
from fastapi import FastAPI, APIRouter, Request, Header, Body, HTTPException, Depends, Query, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, select
from typing import Optional, List, Annotated

# my modules
from database import engine, get_session
from models.todos import Todo, TodoCreate, TodoRead, TodoUpdate, TodoDelete
from models.users import User, UserCreate, UserRead, UserUpdate, UserDelete

# FastAPI instance and API router
app = FastAPI()
router = APIRouter()

# templates settings
templates = Jinja2Templates(directory='templates')

# routes below 000000000000000000000000000000000000


# create
@router.post("/todos", response_model = TodoRead, tags=["Todo"])
def create_todo(*, session: Session = Depends(get_session), todo: TodoCreate):
    db_todo = Todo.from_orm(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo



# read list
@router.get("/todos/json", response_model = List[TodoRead], tags=["Todo"])
def read_todos_list(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
    if not todos:
        raise HTTPException(status_code=404, detail="Not found")
    return todos




# read one
@router.get("/todos/json/{todo_id}", response_model = TodoRead, tags=["Todo"])
def read_todo(*, session: Session = Depends(get_session), todo_id: int):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Not found")
    return todo



# update
@router.patch("/todos/{todo_id}", response_model = TodoRead, tags=["Todo"])
def update_todo(*, session: Session = Depends(get_session), todo_id: int, todo: TodoUpdate):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Not found")
    todo_data = todo.model_dump(exclude_unset=True)
    for key, value in todo_data.todos():
        setattr(db_todo, key, value)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo



# delete
@router.delete("/todos/{todo_id}", tags=["Todo"])
def delete_todo(*, session: Session = Depends(get_session), todo_id: int):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(todo)
    session.commit()
    return {"ok": True}


