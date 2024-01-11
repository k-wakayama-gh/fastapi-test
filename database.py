# --- database.py ---

# modules
from sqlmodel import SQLModel, create_engine, Session
import os

volume_path = "/code/volume1"

if not os.path.exists(volume_path):
    os.makedirs(volume_path)



# database settings
engine = create_engine('sqlite:///volume1_database.sqlite', echo=False, connect_args={'check_same_thread': False})

# def : create the database
def create_database():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


