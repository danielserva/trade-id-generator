from fastapi import APIRouter
from app.identity.generation import generate, generate_bulk
router = APIRouter(
    prefix="/generate",
    tags=["identity"],
)

@router.get("/", tags=["identity"])
async def generate_id():
    # Generate a single 7-character trade ID
    return generate()

@router.get("/bulk/{bulk_size}", tags=["identity"])
async def generate_bulk_id(bulk_size: int):
    # Generate multiple trade IDs in bulk
    return generate_bulk(bulk_size)