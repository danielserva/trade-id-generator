# -*- coding: utf-8 -*-

import re
import mock
import pytest
from concurrent.futures import ThreadPoolExecutor
from app.identity.generation import TradeIdGenerator
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.identity.generation import TradeIdGenerator
from app.database import GeneratedId

ID_CHARACTERS = '0ABCDEFG'

trade_id_generator = TradeIdGenerator()

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.mark.timeout(6000)
def test_generate_bulk_performance(session: Session):
    """This needs to run in a clean enironment, so if you are using any
    external persistence, clear it before running this."""
    with mock.patch('app.identity.generation.ID_CHARACTERS', ID_CHARACTERS):
        ids = list(trade_id_generator.generate_bulk(bulk_size=2097100, session=session))
    assert True

@pytest.mark.timeout(60)
def test_generate_small_bulk_performance(session: Session):
    """This needs to run in a clean enironment, so if you are using any
    external persistence, clear it before running this."""
    with mock.patch('app.identity.generation.ID_CHARACTERS', ID_CHARACTERS):
        ids = list(trade_id_generator.generate_bulk(bulk_size=20971, session=session))
    assert True
