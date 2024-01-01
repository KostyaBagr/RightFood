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


def add_dish(food: schemas.BaseFood, db: Session = (Depends(get_db))):
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


def create_food_list(db: Session, food_list_create: schemas.CreateDailyFood):
    """Создание объекта foodlist"""
    db_food_list = FoodList(**food_list_create.dict())
    db.add(db_food_list)
    db.commit()
    db.refresh(db_food_list)
    return db_food_list


def get_food(user_id: int, db: Session):
    """Получени спика еды пользователя"""
    return db.query(FoodList).filter(FoodList.user_id == user_id).first()
