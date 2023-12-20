# --- add_row.py ---

# modules
from sqlmodel import SQLModel, Session, select

from database import engine
from models import items, users, lessons, todos

def add_row():
    sample_item = items.Item(item_name="アイテム名", price=100, description="これはサンプルアイテムです！")
    sample_user = users.User(username="ユーザー名", email="example@mail.com", full_name="John Smith")
    sample_lesson = lessons.Lesson(number=1, title="体操", teacher="講師", day="水", time="10:00〜12:00", price=5000, description="コメント！")
    sample_todo = todos.Todo(title="サンプルタスク", content="内容がないよう")
    
    session = Session(engine)
    
    session.add(sample_item)
    session.add(sample_user)
    session.add(sample_lesson)
    session.add(sample_todo)
    
    
    session.commit()
    
    session.close()

add_row()

