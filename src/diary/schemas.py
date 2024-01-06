from datetime import datetime
from typing import List

from pydantic import BaseModel
from typing import Optional


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


class IntermediateDishBase(BaseModel):
    """Схема для промежуточной модели еды"""
    weight: str


class IntermediateDishList(BaseModel):
    """Схема для чтения IntermediateDish"""
    id: int
    dish_id: int
    dish_name: str
    created_at: datetime
    calories: Optional[str] = None
    fats: Optional[str] = None
    proteins: Optional[str] = None

    breakfast_list_id: Optional[int] = None
    lunch_list_id: Optional[int] = None
    dinner_list_id: Optional[int] = None


class CreateIntermediateDish(IntermediateDishBase):
    """Схема для создания IntermediateDish"""
    breakfast_list_id: int = None
    lunch_list_id: int = None
    dinner_list_id: int = None
    dish_id: int



class CreateMeal(BaseModel):
    """Create breakfast, lunch, dinner"""
    food_list_id: int


class ListMeal(CreateMeal):
    id: int
    intermediate_dishes: List[IntermediateDishList] = []

    class Config:
        orm_mode = True
        from_attributes = True


class CreateDailyFood(BaseModel):
    """Схема для созданиятаблицы FoodList"""
    user_id: int


class GetDailyList(BaseModel):
    """Схема для получения объекта foodlist"""
    id: int
    breakfast: List[ListMeal] = []
    lunch: List[ListMeal] = []
    dinner: List[ListMeal] = []
    created_at: datetime
    valid_to: datetime
    user_id: int

    class Config:
        from_attributes = True
        orm_mode = True







