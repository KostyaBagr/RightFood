from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from src.config.base import Base

breakfast_dish_association = Table(
    'breakfast_dish_association',
    Base.metadata,
    Column('breakfast_id', Integer, ForeignKey('breakfast_lists.id', ondelete='CASCADE')),
    Column('dish_id', Integer, ForeignKey('dishes.id', ondelete='CASCADE')),
    Column('weight', String),
    Column('created_at', DateTime, server_default=func.now()),
)

lunch_dish_association = Table(
    'lunch_dish_association',
    Base.metadata,
    Column('lunch_id', Integer, ForeignKey('lunch_lists.id', ondelete='CASCADE')),
    Column('dish_id', Integer, ForeignKey('dishes.id', ondelete='CASCADE')),
    Column('weight', String),
    Column('created_at', DateTime, server_default=func.now()),
)

dinner_dish_association = Table(
    'dinner_dish_association',
    Base.metadata,
    Column('dinner_id', Integer, ForeignKey('dinner_lists.id', ondelete='CASCADE')),
    Column('dish_id', Integer, ForeignKey('dishes.id', ondelete='CASCADE')),
    Column('weight', String),
    Column('created_at', DateTime, server_default=func.now()),
)


class FoodList(Base):
    """Список еды за день"""
    __tablename__ = 'food_lists'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    valid_to = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user: Mapped['User'] = relationship(back_populates="food_list")


class BreakfastList(Base):
    """Список еды на завтрак"""
    __tablename__ = 'breakfast_lists'

    id = Column(Integer, primary_key=True, index=True)
    dishes = relationship('Dish', secondary=breakfast_dish_association, back_populates='breakfast_lists')
    weight = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    food_list_id = Column(Integer, ForeignKey("food_lists.id"))

class LunchList(Base):
    """Список еды на обед"""
    __tablename__ = 'lunch_lists'

    id = Column(Integer, primary_key=True, index=True)
    dishes = relationship('Dish', secondary=lunch_dish_association, back_populates='lunch_lists')
    weight = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    food_list_id = Column(Integer, ForeignKey("food_lists.id"))

class DinnerList(Base):
    """Список еды на ужин"""
    __tablename__ = 'dinner_lists'

    id = Column(Integer, primary_key=True, index=True)
    dishes = relationship('Dish', secondary=dinner_dish_association, back_populates='dinner_lists')
    weight = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    food_list_id = Column(Integer, ForeignKey("food_lists.id"))


class Category(Base):
    """Категория блюда"""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    dishes = relationship('Dish', back_populates='category')


class Dish(Base):
    """Информация о блюде"""
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    category = relationship('Category', back_populates='dishes')
    breakfast_lists = relationship('BreakfastList', secondary=breakfast_dish_association, back_populates='dishes')
    lunch_lists = relationship('LunchList', secondary=lunch_dish_association, back_populates='dishes')
    dinner_lists = relationship('DinnerList', secondary=dinner_dish_association, back_populates='dishes')
    name = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    calories = Column(String(5), nullable=False)
    fats = Column(String(5), nullable=False)
    proteins = Column(String(5), nullable=False)
    carbohydrates = Column(String(5), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
