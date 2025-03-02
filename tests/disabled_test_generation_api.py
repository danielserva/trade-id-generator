# -*- coding: utf-8 -*-

import re
import pytest
from concurrent.futures import ThreadPoolExecutor
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.identity.generation import TradeIdGenerator
from app.identity.constants import ID_CHARACTERS
from app.main import app, get_session
from app.database import GeneratedId
trade_id_generator = TradeIdGenerator()
format_check = re.compile('^[' + ID_CHARACTERS + ']{7}$')

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_generate_response_is_the_correct_length(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    generated_id =trade_id_generator.generate()
    app.dependency_overrides.clear()
    assert len(generated_id) == 7
