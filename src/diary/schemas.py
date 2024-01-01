from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Optional


class BaseFood(BaseModel):

    category_id: Optional[int] = None
    name: str
    brand: str
    calories: str
    fats: str
    proteins: str
    carbohydrates: str


class FoodList(BaseFood):
    id: int

    class Config:
        orm_mode = True


class BaseCategory(BaseModel):
    name: str
    description: str


class CategoryList(BaseCategory):
    id: int

    class Config:
        orm_mode = True


class CreateDailyFood(BaseModel):
    """Схема для созданиятаблицы FoodList"""

    user_id: int

class GetDailyList(BaseModel):
    """Схема для полчения объекта foodlist"""
    id: int
    created_at: datetime
    valid_to: datetime
    user_id: int

    class Config:
        orm_mode = True

