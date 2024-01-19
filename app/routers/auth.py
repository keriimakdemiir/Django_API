from fastapi import APIRouter, Depends, status, HTTPException
from settings import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


def get_db_conn():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db_conn)]


# region DTOs
class UserDTO(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


# endregion

SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
ALGORITHM = 'HS256'

# pip install bcrypt paketini kuralım
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_dto: UserDTO):
    try:
        user = User(
            email=user_dto.email,
            user_name=user_dto.username,
            first_name=user_dto.first_name,
            last_name=user_dto.last_name,
            hashed_password=pwd_context.hash(user_dto.password),
            is_active=True,
            role=user_dto.role
        )

        db.add(user)
        db.commit()
        # print(create_access_token('beast'))
        return {
            'status_code': 201,
            'transaction': 'Successfull'
        }
    except Exception as err:
        return {
            'error': err
        }


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {
        'sub': username,
        'id': user_id,
        'role': role
    }

    expires = datetime.utcnow() + expires_delta

    encode.update({
        'exp': expires
    })

    # pip install python-jose
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(user_name: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.user_name == user_name).first()

    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False

    return user


@router.post('/token')
async def get_access_token(db: db_dependency, from_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(from_data.username, from_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )
    else:
        token = create_access_token(user.user_name, user.id, user.role, timedelta(minutes=30))

    return {
        'access_token': token,
        'token_type': 'bearer'
    }
