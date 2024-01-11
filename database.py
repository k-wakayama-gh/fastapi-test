# --- database.py ---

# modules
from sqlmodel import SQLModel, create_engine, Session

# database settings
engine = create_engine('sqlite:///database.sqlite', echo=False, connect_args={'check_same_thread': False})

# def : create the database
def create_database():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


