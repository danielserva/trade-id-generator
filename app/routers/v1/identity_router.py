from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import SQLModel, Session
from app.identity.generation import TradeIdGenerator
from app.dependencies import get_session

SessionDep = Annotated[Session, Depends(get_session)]

class BulkResponse(SQLModel):
    ids: list[str]
    count: int

trade_id_generator = TradeIdGenerator()
router = APIRouter(
    prefix="/generate",
    tags=["identity"],
)

@router.get("/", tags=["identity"])
async def generate_id(session: SessionDep):
    # Generate a single 7-character trade ID
    return trade_id_generator.generate(session)

@router.post("/bulk/{bulk_size}", response_model=BulkResponse, tags=["identity"])
async def generate_bulk_id(bulk_size: int, session: SessionDep):
    # Generate multiple trade IDs in bulk
    generated_ids = trade_id_generator.generate_bulk(bulk_size, session)
    response = BulkResponse(ids=generated_ids,count=len(generated_ids))
    return response