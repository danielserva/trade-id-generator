from typing import Set
from .database import engine
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session

# Local cache for performance optimization
cached_ids: Set[str] = set()