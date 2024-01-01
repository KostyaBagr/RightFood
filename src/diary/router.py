from typing import List

from fastapi import APIRouter
from .services import get_dish_list, add_dish, category_list, add_category, create_food_list, get_food
from database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from src.diary import schemas

router = APIRouter()


@router.get("/dish_list/", response_model=List[schemas.FoodList])
def dish_list(limit: int, db: Session = (Depends(get_db)), category_id: int = None):
    """GET food"""
    return get_dish_list(limit=limit, db=db, category_id=category_id)


@router.post("/create_dish/", response_model=schemas.BaseFood)
def create_dish(food: schemas.BaseFood, db: Session = (Depends(get_db))):
    """CREATE food"""
    return add_dish(food=food, db=db)


@router.get("/categories/", response_model=List[schemas.CategoryList])
def get_categories(db: Session = (Depends(get_db))):
    """GET categories"""
    return category_list(db=db)


@router.post("/categories/", response_model=schemas.BaseCategory)
def create_category(category: schemas.BaseCategory, db: Session = (Depends(get_db))):
    """CREATE category"""
    return add_category(db=db, category=category)


@router.post("/create_food_list/", response_model=schemas.CreateDailyFood)
def add_food_list(food_list_create: schemas.CreateDailyFood, db: Session = Depends(get_db)):
    """CREATE FoodList"""
    return create_food_list(db, food_list_create)


@router.get("/user_food_list/", response_model=schemas.GetDailyList)
def get_daily_food_list(user_id: int, db:Session = Depends(get_db)):
    """GET FoodList"""
    return get_food(db=db, user_id=user_id)