from fastapi import APIRouter, Depends, status
from settings import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import User
from passlib.context import CryptContext

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db_conn():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db_conn)]


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency):
    return db.query(User).all()