from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,ForeignKey, Integer, String, DateTime, Table, Boolean
from sqlalchemy.orm import relationship, Mapped
from src.config.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=True)
    age = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    height = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    food_list: Mapped[List["FoodList"]] = relationship(back_populates="user")

