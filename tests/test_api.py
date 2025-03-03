# -*- coding: utf-8 -*-

import re
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.dependencies import get_session
from app.identity.constants import ID_CHARACTERS
from app.main import app
from app.routers.v1.identity_router import BulkResponse
format_check = re.compile('^[' + ID_CHARACTERS + ']{7}$')

client = TestClient(app)

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_app_starts_successfully(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    response = client.get("/")
    app.dependency_overrides.clear()
    assert response.status_code == 200

def test_generate_response_is_the_correct_length_and_format(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    response = client.get("/generate")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    generated_id = response.json()
    assert len(generated_id) == 7
    assert format_check.match(generated_id) is not None

def test_generate_bulk_response_is_the_correct_length_and_format(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    bulk_size_test = 100
    response = client.post(f"/generate/bulk/{bulk_size_test}")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    # Validation using Pydantic model
    bulk_response = BulkResponse(**response.json())
    assert len(bulk_response.ids) == bulk_size_test
    assert bulk_response.count == bulk_size_test
    assert all(format_check.match(generated_id) is not None for generated_id in bulk_response.ids)
