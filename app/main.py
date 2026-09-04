from fastapi import FastAPI,Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.v1.router import router as api_router

from app.db.session import get_db

app = FastAPI()
title = "Notes management stystem"
version = "0.1.0"

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Notes management system!"}

