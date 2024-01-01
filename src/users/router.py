from fastapi import Depends
from src.users import schemas
from sqlalchemy.orm import Session
from fastapi import APIRouter
from database import get_db
from src.users.models import User

router = APIRouter()




@router.get("/users/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """Get users by filter"""
    return db.query(User).offset(skip).limit(limit).all()


@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUserRequest, db: Session = Depends(get_db)):
    """Создание пользователя"""
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
