from fastapi import APIRouter
from app.identity.generation import generate
router = APIRouter(
    prefix="/identity",
    tags=["identity"],
)

@router.get("/", tags=["identity"])
async def generate_id():
    return generate()