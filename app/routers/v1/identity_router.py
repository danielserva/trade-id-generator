from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.identity.generation import generate, generate_bulk
from app.main import SessionDep

router = APIRouter(
    prefix="/generate",
    tags=["identity"],
)

@router.get("/", tags=["identity"])
async def generate_id(session: SessionDep):
    # Generate a single 7-character trade ID
    return generate()

@router.get("/bulk/{bulk_size}", tags=["identity"])
async def generate_bulk_id(bulk_size: int, session: SessionDep):
    # Generate multiple trade IDs in bulk
    return generate_bulk(bulk_size)