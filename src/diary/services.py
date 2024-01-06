from typing import Type, Union
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database import get_db
from fastapi import Depends
from src.diary.models import Dish, Category, FoodList, BreakfastList, LunchList, DinnerList, IntermediateDish
from src.diary import schemas


def get_dish_list(limit: int, db: Session = (Depends(get_db)), category_id: int = None):
    """Получение списка блюд
    limit - Лимит по выдаче блюд
    db - БД
    category_id - опциональный парамерт для фильтрации по категориям"""
    if category_id is not None:
        return db.query(Dish).filter(Dish.category_id == category_id).limit(limit).all()
    else:
        return db.query(Dish).limit(limit).all()


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


    food_list = db.query(FoodList).filter(FoodList.id == food_list_id).first()

    if food_list:
        breakfast = db.query(BreakfastList).filter(BreakfastList.food_list_id == food_list.id).options(joinedload(BreakfastList.intermediate_dishes)).first()
        lunch = db.query(LunchList).filter(LunchList.food_list_id == food_list.id).options(joinedload(LunchList.intermediate_dishes)).first()
        dinner = db.query(DinnerList).filter(DinnerList.food_list_id == food_list.id).options(joinedload(DinnerList.intermediate_dishes)).first()

        if breakfast:
            intermediate_breakfast_dishes = breakfast.intermediate_dishes
        else:
            intermediate_breakfast_dishes = []

        if lunch:
            intermediate_lunch_dishes = lunch.intermediate_dishes
        else:
            intermediate_lunch_dishes = []

        if dinner:
            intermediate_dinner_dishes = dinner.intermediate_dishes
        else:
            intermediate_dinner_dishes = []

        response_data = {
            "id": food_list.id,
            "created_at": food_list.created_at,
            "valid_to": food_list.valid_to,
            "user_id": food_list.user_id,
            "breakfast": [
                {
                    "id": breakfast.id,
                    "created_at": breakfast.created_at,
                    "food_list_id": breakfast.food_list_id,
                    "intermediate_dishes": [
                        {
                            "id": dish.id,
                            "dish_id": dish.dish_id,
                            "dish_name": dish.dish.name,
                            "weight": dish.weight,
                            "calories": dish.calories,
                            "fats": dish.fats,
                            "proteins": dish.proteins,
                            "breakfast_list_id": dish.breakfast_list_id if dish.breakfast_list_id else None,
                            "created_at": dish.created_at,
                        }
                        for dish in intermediate_breakfast_dishes
                    ],
                }
            ],
            "lunch": [
                {
                    "id": lunch.id,
                    "created_at": lunch.created_at,
                    "food_list_id": lunch.food_list_id,
                    "intermediate_dishes": [
                        {
                            "id": dish.id,
                            "dish_id": dish.dish_id,
                            "dish_name": dish.dish.name,
                            "weight": dish.weight,
                            "calories": dish.calories,
                            "fats": dish.fats,
                            "proteins": dish.proteins,
                            "lunch_list_id": dish.lunch_list_id if dish.lunch_list_id else None,
                            "created_at": dish.created_at,
                        }
                        for dish in intermediate_lunch_dishes
                    ],
                }
            ],
            "dinner": [
                {
                    "id": dinner.id,
                    "created_at": dinner.created_at,
                    "food_list_id": dinner.food_list_id,
                    "intermediate_dishes": [
                        {
                            "id": dish.id,
                            "dish_id": dish.dish_id,
                            "dish_name": dish.dish.name,
                            "weight": dish.weight,
                            "calories": dish.calories,
                            "fats": dish.fats,
                            "proteins": dish.proteins,
                            "dinner_list_id": dish.dinner_list_id if dish.dinner_list_id else None,
                            "created_at": dish.created_at,
                        }
                        for dish in intermediate_dinner_dishes
                    ],
                }
            ],
        }

        return response_data

    else:
        return {"error": "Food list not found for the given user_id"}


def create_meal(data: schemas.CreateMeal, db: Session, model: Type[Union[BreakfastList, LunchList, DinnerList]]):
    """Создание объекта приема пищи. Breakfast, lunch, dinner"""

    meal = model(
        food_list_id=data.food_list_id,

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


def create_intermediate_dish(data: schemas.CreateIntermediateDish, db: Session):
    """Создание объекта intermediate dish"""
    db_inter_dish = IntermediateDish(
        dish_id=data.dish_id,
        breakfast_list_id=data.breakfast_list_id if data.breakfast_list_id else None,
        lunch_list_id=data.lunch_list_id if data.lunch_list_id else None,
        dinner_list_id=data.dinner_list_id if data.dinner_list_id else None,
        weight=data.weight
    )
    db.add(db_inter_dish)
    db.commit()
    db.refresh(db_inter_dish)
    return db_inter_dish


def get_intermediate_dish(inter_dish_id: int, db: Session):
    """Получение объекта intermediate dish"""
    return db.query(IntermediateDish).filter(IntermediateDish.id == inter_dish_id).first()
