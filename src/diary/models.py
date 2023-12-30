from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from src.config.base import Base


breakfast_food_association = Table(
    'breakfast_food_association',
    Base.metadata,
    Column('breakfast_id', Integer, ForeignKey('breakfast_lists.id')),
    Column('food_id', Integer, ForeignKey('foods.id')),
    Column('weight', String),
    Column('created_at', DateTime, server_default=func.now()),
)

lunch_food_association = Table(
    'lunch_food_association',
    Base.metadata,
    Column('lunch_id', Integer, ForeignKey('lunch_lists.id')),
    Column('food_id', Integer, ForeignKey('foods.id')),
    Column('weight', String),
    Column('created_at', DateTime, server_default=func.now()),
)

dinner_food_association = Table(
    'dinner_food_association',
    Base.metadata,
    Column('dinner_id', Integer, ForeignKey('dinner_lists.id')),
    Column('food_id', Integer, ForeignKey('foods.id')),
    Column('weight', String),
    Column('created_at', DateTime, server_default=func.now()),
)


class FoodList(Base):
    """Список еды за день"""
    __tablename__ = 'food_lists'

    id = Column(Integer, primary_key=True, index=True)
    breakfast = Column(Integer, ForeignKey("breakfast_lists.id"))
    lunch = Column(Integer, ForeignKey("lunch_lists.id"))
    dinner = Column(Integer, ForeignKey("dinner_lists.id"))
    created_at = Column(DateTime, server_default=func.now())
    valid_to = Column(DateTime, server_default=func.now())


class BreakfastList(Base):
    """Список еды на завтрак"""
    __tablename__ = 'breakfast_lists'

    id = Column(Integer, primary_key=True, index=True)
    foods = relationship('Food', secondary=breakfast_food_association, back_populates='breakfast_lists')
    weight = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class LunchList(Base):
    """Список еды на обед"""
    __tablename__ = 'lunch_lists'

    id = Column(Integer, primary_key=True, index=True)
    foods = relationship('Food', secondary=lunch_food_association, back_populates='lunch_lists')
    weight = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class DinnerList(Base):
    """Список еды на ужин"""
    __tablename__ = 'dinner_lists'

    id = Column(Integer, primary_key=True, index=True)
    foods = relationship('Food', secondary=dinner_food_association, back_populates='dinner_lists')
    weight = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Food(Base):
    """Информация о блюде"""
    __tablename__ = 'foods'

    id = Column(Integer, primary_key=True, index=True)
    breakfast_lists = relationship('BreakfastList', secondary=breakfast_food_association, back_populates='foods')
    lunch_lists = relationship('LunchList', secondary=lunch_food_association, back_populates='foods')
    dinner_lists = relationship('DinnerList', secondary=dinner_food_association, back_populates='foods')
    name = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    calories = Column(String(5), nullable=False)
    fats = Column(String(5), nullable=False)
    proteins = Column(String(5), nullable=False)
    carbohydrates = Column(String(5), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
