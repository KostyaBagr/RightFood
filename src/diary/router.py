from typing import List
from .models import BreakfastList, LunchList, DinnerList, FoodList
from fastapi import APIRouter
from .services import get_dish_list, add_dish, category_list, add_category, create_food_list, get_food_list, \
    create_meal
from database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from src.diary import schemas

router = APIRouter()


@router.get("/dish_list/", response_model=List[schemas.DishList])
def dish_list(limit: int, db: Session = (Depends(get_db)), category_id: int = None):
    """GET food"""
    return get_dish_list(limit=limit, db=db, category_id=category_id)


@router.post("/create_dish/", response_model=schemas.BaseDish)
def create_dish(food: schemas.BaseDish, db: Session = (Depends(get_db))):
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
def get_daily_food_list(food_list_id: int = None, db: Session = Depends(get_db)):
    """GET FoodList"""

    return get_food_list(db=db, food_list_id=food_list_id)


@router.post("/create_breakfast_list/", response_model=schemas.CreateMeal)
def add_breakfast_list(data: schemas.CreateMeal, db: Session = Depends(get_db)):
    """CREATE BreakfastList"""

    return create_meal(data=data, db=db, model=BreakfastList)


@router.post("/create_lunch_list/", response_model=schemas.CreateMeal)
def add_lunch_list(data: schemas.CreateMeal, db: Session = Depends(get_db)):
    """CREATE LunchList"""
    return create_meal(data=data, db=db, model=LunchList)


@router.post("/create_dinner_list/", response_model=schemas.CreateMeal)
def add_dinner_list(data: schemas.CreateMeal, db: Session = Depends(get_db)):
    """CREATE DinnerList"""
    return create_meal(data=data, db=db, model=DinnerList)


