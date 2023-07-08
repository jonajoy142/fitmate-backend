
import sys


sys.path.append("../../")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.server.database import engine
from app.utils import get_db
from starlette import status
from datetime import datetime
from pytz import timezone

import app.server.models as models
import app.users.user_utils as user_utils



foodItemRouter = APIRouter(prefix="/food/details")

models.base.metadata.create_all(bind=engine)

#add data
@foodItemRouter.post('/add/{user_id}')
async def add_biomatrix_data(user_id:int ,data: user_utils.FoodItems, db_session: Session = Depends(get_db)):
    if user_id == None or data.calories == None or data.food_type == None or data.food_name == None or data.quantity == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Some fields are empty")
    ex_user = db_session.query(models.User).filter(models.User.id == user_id).first()
    if not ex_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized to use this route")
    
    new_food_data = models.FoodItems()
    new_food_data.food_name = data.food_name
    new_food_data.user_id = user_id
    new_food_data.food_type = data.food_type
    new_food_data.calories = data.calories
    new_food_data.quantity = data.quantity


    # Convert the current time to India time zone
    india_time = datetime.now(timezone("Asia/Kolkata"))

    new_food_data.food_time = india_time

    db_session.add(new_food_data)
    db_session.commit()

    db_session.refresh(new_food_data)

    if not new_food_data.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="some error occured")
    return {"status": "OK","code":status.HTTP_200_OK,"message":"food data created successfully"}

#read data
@foodItemRouter.post('/read/{user_id}')
async def read_biomatrix_data(user_id: int, db_session: Session = Depends(get_db)):
    ex_user = db_session.query(models.User).filter(models.User.id == user_id).first()
    if not ex_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized to use this route")
    food_data = db_session.query(models.FoodItems).filter(models.FoodItems.user_id == user_id).all()

    if not food_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data not found")
    return {"status": "OK","code":status.HTTP_200_OK,"data":food_data}
