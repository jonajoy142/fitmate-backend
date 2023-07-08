import sys
sys.path.append("../../")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.server.database import engine
from app.utils import get_db
from starlette import status

import app.server.models as models
import app.users.user_utils as user_utils


bioMetrixRouter = APIRouter(prefix="/biometrix")

models.base.metadata.create_all(bind=engine)

# add biometrix
@bioMetrixRouter.post('/add/{user_id}')
async def add_biomatrix_data(user_id:int ,data: user_utils.BioMatricData, db_session: Session = Depends(get_db)):
    if user_id == None or data.age == None or data.height == None or data.weight == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Some fields are empty")
    ex_user = db_session.query(models.User).filter(models.User.id == user_id).first()
    if not ex_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized to use this route")
    new_bio_data = models.BioMetrix()
    new_bio_data.user_id = user_id
    new_bio_data.age = data.age
    new_bio_data.height = data.height
    new_bio_data.weight = data.weight
    new_bio_data.bmi = (data.weight / (data.height ** 2))

    db_session.add(new_bio_data)
    db_session.commit()

    db_session.refresh(new_bio_data)

    if not new_bio_data.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="some error occured")
    return {"status": "OK","code":status.HTTP_200_OK,"message":"Biodata created successfully"}
# read biometrix
@bioMetrixRouter.post('/read/{user_id}')
async def read_biomatrix_data(user_id: int, db_session: Session = Depends(get_db)):
    ex_user = db_session.query(models.User).filter(models.User.id == user_id).first()
    if not ex_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized to use this route")
    bio_matrix_data = db_session.query(models.BioMetrix).filter(models.BioMetrix.user_id == user_id).first()

    if not bio_matrix_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data not found")
    
    return {"status": "OK","code":status.HTTP_200_OK,"data":bio_matrix_data}

@bioMetrixRouter.put('/update/{user_id}')
async def update_biomatrix_data(user_id: int,data: user_utils.UpdateBioMatricData, db_session: Session = Depends(get_db)):
    ex_user = db_session.query(models.User).filter(models.User.id == user_id).first()
    if not ex_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized to use this route")
    bio_matrix_data = db_session.query(models.BioMetrix).filter(models.BioMetrix.user_id == user_id).first()

    if not bio_matrix_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="data not found")
    
    bio_matrix_data.age = data.age if data.age is not None else bio_matrix_data.age
    bio_matrix_data.height = data.height if data.height is not None else bio_matrix_data.height
    bio_matrix_data.weight = data.weight if data.weight is not None else bio_matrix_data.weight

    bio_matrix_data.bmi = (bio_matrix_data.weight / (bio_matrix_data.height ** 2))

    db_session.commit()

    db_session.refresh(bio_matrix_data)
    if not bio_matrix_data.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="some error occured")
    return {"status": "OK","code":status.HTTP_200_OK,"message":"Biodata updated successfully","data":bio_matrix_data}