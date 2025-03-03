# -*- coding: utf-8 -*-

import re
import pytest
from concurrent.futures import ThreadPoolExecutor
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.identity.generation import TradeIdGenerator
from app.identity.constants import ID_CHARACTERS
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


def test_id_is_the_correct_length(session: Session):
    generated_id =trade_id_generator.generate(session)
    assert len(generated_id) == 7


def test_id_uses_correct_characters(session: Session):
    generated_id = trade_id_generator.generate(session)
    assert format_check.match(generated_id) is not None


def test_ids_are_unique_and_correct_format(session: Session):
    ids = set()
    generated_count = 0
    while generated_count < 22000:
        generated_id = trade_id_generator.generate(session)
        generated_count += 1
        assert generated_id not in ids
        ids.add(generated_id)
        assert format_check.match(generated_id) is not None


def test_ids_are_unique_generated_in_bulk(session: Session):
    generated_ids = set()
    generated_count = 0
    while generated_count < 100:
        generated_ids.update(trade_id_generator.generate_bulk(bulk_size=1000, session=session))
        generated_count += 1
        assert len(generated_ids) == generated_count * 1000

""" Disabled due to Sqlite concurrency limitation.
Re-enable after replacing sqlite with a more concurrency friendly database like PostgreSql """
def disabled_test_concurrent_bulk_generation():
    generated_ids = set()
    bulk_args = []
    sqlite_file_name = "testing_concurrent.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(
        sqlite_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool)
    
    """Enable WAL mode for better concurrency
    ATTENTION: THIS IS SPECIFIC FOR SQLITE"""
    with engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA journal_mode=WAL;")
        conn.exec_driver_sql("PRAGMA synchronous=NORMAL;")
        conn.exec_driver_sql("PRAGMA busy_timeout=5000;")
    
    SQLModel.metadata.create_all(engine)
    
    # Create fewer but larger batches
    for _ in range(5): #  Reduce from 2000 to 5
        bulk_args.append(10000) # 10k per batch instead of 2.5k

    def generate_with_new_session(count):
        local_generator = TradeIdGenerator()
        with Session(engine) as session:
            return local_generator.generate_bulk(bulk_size=count, session=session)

    def consumer_function(ids):
        return list(ids)

    with ThreadPoolExecutor(max_workers=2) as pool:
        generators = list(pool.map(generate_with_new_session, bulk_args))
        ids = list(pool.map(consumer_function, generators))

        for chunk in ids:
            generated_ids.update(chunk)

    assert len(generated_ids) == 50000