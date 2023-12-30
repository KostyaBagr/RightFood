from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter
from database import get_db
from src.users.models import User

router = APIRouter()


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

class CreateUserRequest(BaseModel):
    email: str
    hashed_password: str
    is_active: bool

@router.get("/users/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """Get users by filter"""
    return db.query(User).offset(skip).limit(limit).all()


@router.post("/users/", response_model=UserResponse)
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    """Создание пользователя"""
    db_user = User(**user.dict())  # Convert CreateUserRequest to User
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
