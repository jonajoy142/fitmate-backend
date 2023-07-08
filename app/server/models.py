import sys
sys.path.append("../../")

from app.server.database import base
from sqlalchemy import Column,String,Integer,Float,DateTime,ForeignKey
from datetime import datetime

class User(base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

class BioMetrix(base):
    __tablename__ = "user_biomatrix"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"), nullable=False)
    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)
    bmi = Column(Float)

class FoodItems(base):
    __tablename__ = "food_items"
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"), nullable=False)
    food_name = Column(String)
    food_type = Column(String)
    quantity = Column(Float)
    calories = Column(Float)
    food_time = Column(DateTime)
    
