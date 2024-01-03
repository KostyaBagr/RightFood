from typing import Type, Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import get_db
from fastapi import Depends
from src.diary.models import Dish, Category, FoodList, BreakfastList, LunchList, DinnerList
from src.diary import schemas


def get_dish_list(limit: int, db: Session = (Depends(get_db)), category_id: int = None):
    """Получение списка блюд
    limit - Лимит по выдаче блюд
    db - БД
    category_id - опциональный парамерт для фильтрации по категориям"""
    return db.query(Dish).filter(Dish.category_id == category_id).limit(limit).all()


def add_dish(food: schemas.BaseDish, db: Session = (Depends(get_db))):
    """Добавление блюда(не в ежедневный список еды)"""
    food_db = Dish(
        category_id=food.category_id,
        name=food.name,
        brand=food.brand,
        calories=food.calories,
        fats=food.fats,
        proteins=food.proteins,
        carbohydrates=food.carbohydrates
    )
    db.add(food_db)
    db.commit()
    db.refresh(food_db)
    return food_db


def category_list(db: Session = (Depends(get_db))):
    """Получние списка категорий"""
    return db.query(Category).all()


def add_category(category: schemas.BaseCategory, db: Session = (Depends(get_db))):
    """Создание новой категории"""
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def create_food_list(food_list_create: schemas.CreateDailyFood, db: Session):
    """Создание объекта foodlist"""
    db_food_list = FoodList(**food_list_create.dict())
    db.add(db_food_list)
    db.commit()
    db.refresh(db_food_list)
    return db_food_list


def get_food_list(db: Session, food_list_id: int = None):
    """Получение спика еды пользователя за день"""

    # добавить: получение еды именно для текущего пользователя
    food_list = db.query(FoodList).filter(FoodList.id == food_list_id).first()

    if food_list:
        breakfast = db.query(BreakfastList).filter(BreakfastList.food_list_id == food_list.id).all()
        lunch = db.query(LunchList).filter(LunchList.food_list_id == food_list.id).all()
        dinner = db.query(DinnerList).filter(DinnerList.food_list_id == food_list.id).all()

        response_data = {
            "id": food_list.id,
            "created_at": food_list.created_at,
            "valid_to": food_list.valid_to,
            "user_id": food_list.user_id,
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
        }

        return response_data
    else:
        return {"error": "Food list not found for the given user_id"}


def create_meal(data: schemas.CreateMeal, db: Session, model: Type[Union[BreakfastList, LunchList, DinnerList]]):
    """Создание объекта приема пищи. Breakfast, lunch, dinner"""

    meal = model(
        weight=data.weight,
        food_list_id=data.food_list_id,
        dishes=data.dishes if data.dishes is not None else []
    )
    food_list = db.query(FoodList).filter(FoodList.id == data.food_list_id).first()

    if not food_list:
        return {"error": "FoodList not found"}
    else:
        if model == BreakfastList:
            food_list.breakfast = meal
        elif model == LunchList:
            food_list.lunch = meal
        elif model == DinnerList:
            food_list.dinner = meal
        else:
            return {"error": "unknown model"}

    db.commit()

    return meal
