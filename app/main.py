from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from .routers.v1 import identity_router
from .database import create_db_and_tables
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Trade ID Generator API",
    description="This application generates random 7 character human-readable IDs. It can generate in a single or bulk mode",
    version="1.0.0",
    lifespan=lifespan
)

# API routes
app.include_router(identity_router.router)

@app.get("/", tags=["Info"])
async def root():
    """Get API information"""
    return {
        "name": "Trade Id generator",
        "description": "This application generates unique human readable Ids for currency trades",
        "endpoints": [
            {"path": "/generate", "method": "GET", "description": "Generate a single trade ID"},
            {"path": "/generate/bulk", "method": "POST", "description": "Generate multiple trade IDs in bulk"}
        ]
    }