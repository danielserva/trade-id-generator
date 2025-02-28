from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import List, Set
import uvicorn

app = FastAPI(
    title="Trade ID Generator API",
    description="This application generates random 7 character human-readable IDs. It can generate in a single or bulk mode",
    version="1.0.0"
)

# API routes
@app.get("/", tags=["Info"])
async def root():
    """Get API information"""
    return {
        "name": "Human readable Trade Id generator",
        "description": "Generates unique human readable Ids for currency trades",
    }
