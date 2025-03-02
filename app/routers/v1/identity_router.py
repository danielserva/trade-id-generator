from fastapi import APIRouter, Depends
from app.identity.generation import TradeIdGenerator
from app.main import SessionDep

trade_id_generator = TradeIdGenerator()
router = APIRouter(
    prefix="/generate",
    tags=["identity"],
)

@router.get("/", tags=["identity"])
async def generate_id(session: SessionDep):
    # Generate a single 7-character trade ID
    return trade_id_generator.generate(session)

@router.get("/bulk/{bulk_size}", tags=["identity"])
async def generate_bulk_id(bulk_size: int, session: SessionDep):
    # Generate multiple trade IDs in bulk
    return trade_id_generator.generate_bulk(bulk_size, session)