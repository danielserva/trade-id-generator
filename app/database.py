from sqlmodel import SQLModel, Field, create_engine, Session
import time

sqlite_file_name = 'identity.db'
sqlite_url = f"sqlite:///{sqlite_file_name}"

class GeneratedId(SQLModel, table=True):
    id: str = Field(primary_key=True)
    created_at: str = Field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))

connection_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connection_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
