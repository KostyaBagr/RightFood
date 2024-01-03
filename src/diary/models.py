from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func
from src.config.base import Base

breakfast_intermediate_dish_association = Table(
    'breakfast_intermediate_dish_association', Base.metadata,
    Column('breakfast_list_id', Integer, ForeignKey('breakfast_lists.id')),
    Column('intermediate_dish_id', Integer, ForeignKey('intermediate_dishes.id'))
)

lunch_intermediate_dish_association = Table(
    'lunch_intermediate_dish_association', Base.metadata,
    Column('lunch_list_id', Integer, ForeignKey('lunch_lists.id')),
    Column('intermediate_dish_id', Integer, ForeignKey('intermediate_dishes.id'))
)

dinner_intermediate_dish_association = Table(
    'dinner_intermediate_dish_association', Base.metadata,
    Column('dinner_list_id', Integer, ForeignKey('dinner_lists.id')),
    Column('intermediate_dish_id', Integer, ForeignKey('intermediate_dishes.id'))
)


class FoodList(Base):
    """Список еды за день"""
    __tablename__ = 'food_lists'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    valid_to = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user: Mapped['User'] = relationship('User', back_populates="food_list")
    breakfast = relationship('BreakfastList', back_populates='food_list', uselist=False, cascade="all, delete")
    lunch = relationship('LunchList', back_populates='food_list', uselist=False, cascade="all, delete")
    dinner = relationship('DinnerList', back_populates='food_list', uselist=False, cascade="all, delete")


class BreakfastList(Base):
    """Список еды на завтрак"""
    __tablename__ = 'breakfast_lists'

    id = Column(Integer, primary_key=True, index=True)
    intermediate_dishes = relationship('IntermediateDish', back_populates='breakfast_lists')
    created_at = Column(DateTime, server_default=func.now())
    food_list = relationship('FoodList', back_populates='breakfast')
    food_list_id = Column(Integer, ForeignKey("food_lists.id"), unique=True)


class LunchList(Base):
    """Список еды на обед"""
    __tablename__ = 'lunch_lists'

    id = Column(Integer, primary_key=True, index=True)
    intermediate_dishes = relationship('IntermediateDish', back_populates='lunch_lists')
    food_list = relationship('FoodList', back_populates='lunch')
    created_at = Column(DateTime, server_default=func.now())
    food_list_id = Column(Integer, ForeignKey("food_lists.id"), unique=True)


class DinnerList(Base):
    """Список еды на ужин"""
    __tablename__ = 'dinner_lists'

    id = Column(Integer, primary_key=True, index=True)
    intermediate_dishes = relationship('IntermediateDish', back_populates='dinner_lists')
    food_list = relationship('FoodList', back_populates='dinner')
    created_at = Column(DateTime, server_default=func.now())
    food_list_id = Column(Integer, ForeignKey("food_lists.id"), unique=True)


class Category(Base):
    """Категория блюда"""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    dishes = relationship('Dish', back_populates='category')


class IntermediateDish(Base):
    """Промежуточная модель еды для добавления ее в список BreakfastList, LunchList, DinnerList"""

    __tablename__ = 'intermediate_dishes'

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(String, nullable=False)
    dish_id = Column(Integer, ForeignKey("dishes.id"))
    dish = relationship('Dish', back_populates="intermediate_dish")
    created_at = Column(DateTime, server_default=func.now())

    calories = Column(String(5), nullable=False)
    fats = Column(String(5), nullable=False)
    proteins = Column(String(5), nullable=False)

    breakfast_list_id = Column(Integer, ForeignKey("breakfast_lists.id"))
    breakfast_lists = relationship('BreakfastList', back_populates='intermediate_dishes')

    lunch_list_id = Column(Integer, ForeignKey("lunch_lists.id"))
    lunch_lists = relationship('LunchList', back_populates='intermediate_dishes')

    dinner_list_id = Column(Integer, ForeignKey("dinner_lists.id"))
    dinner_lists = relationship('DinnerList', back_populates='intermediate_dishes')


class Dish(Base):
    """Информация о блюде"""
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    category = relationship('Category', back_populates='dishes')
    intermediate_dish = relationship('IntermediateDish', back_populates='dishes')
    name = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    calories = Column(String(5), nullable=False)
    fats = Column(String(5), nullable=False)
    proteins = Column(String(5), nullable=False)
    carbohydrates = Column(String(5), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
