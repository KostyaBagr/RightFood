from datetime import datetime
from typing import List

from pydantic import BaseModel
from typing_extensions import Optional


class BaseDish(BaseModel):
    """Схема для модели Dish"""
    category_id: Optional[int] = None
    name: str
    brand: str
    calories: str
    fats: str
    proteins: str
    carbohydrates: str


class DishList(BaseDish):
    """Схема для модели Dish"""
    id: int

    class Config:
        from_attributes = True


class BaseCategory(BaseModel):
    name: str
    description: str


class CategoryList(BaseCategory):
    id: int

    class Config:
        from_attributes = True


class CreateMeal(BaseModel):
    """Create breakfast, lunch, dinner"""
    food_list_id: int
    weight: str
    dishes: List[DishList] = None


class ListMeal(CreateMeal):
    id: int


class CreateDailyFood(BaseModel):
    """Схема для созданиятаблицы FoodList"""
    user_id: int


class GetDailyList(BaseModel):
    """Схема для полчения объекта foodlist"""
    id: int
    breakfast: List[ListMeal] = []
    lunch: List[ListMeal] = []
    dinner: List[ListMeal] = []
    created_at: datetime
    valid_to: datetime
    user_id: int

    class Config:
        from_attributes = True
