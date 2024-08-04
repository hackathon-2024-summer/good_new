from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db_session import get_db

router = APIRouter(tags=["Develop"])

DbDependency = Annotated[AsyncSession, Depends(get_db)]

@router.get("/")
def read_root():
    return {"Hello": "ngrok World"}
