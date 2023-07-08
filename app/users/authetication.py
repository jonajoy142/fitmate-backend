import sys
sys.path.append("../../")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.server.database import engine
from app.utils import get_db
from starlette import status

import app.server.models as models
import app.users.user_utils as user_utils
import app.users.utils as utils

authRouter = APIRouter(prefix="/auth")

models.base.metadata.create_all(bind=engine)

# route for sign up
@authRouter.post(path="/signup")
async def user_signup(user: user_utils.User, db_session: Session = Depends(get_db)):
    if user.name == None or user.email == None or user.password == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Some fields are empty")

    ex_user = db_session.query(models.User).filter(models.User.email == user.email).first()
    print("Ex user : ",ex_user)
    if ex_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user already existing.") 
    # create new model
    new_user = models.User()
    new_user.name = user.name
    new_user.email = user.email
    new_user.password = utils.get_hash_password(user.password)

    db_session.add(new_user)
    db_session.commit()

    db_session.refresh(new_user)

    if not new_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="some error occured")
    
    return {"status": "OK","code":status.HTTP_200_OK,"message":"New user created successfully"}

# route for sign in
@authRouter.post(path='/signin')
async def user_signin(user: user_utils.SignInForm, db_session: Session = Depends(get_db)):
    if user.email == None or user.password == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Some fields are empty")
    ex_user = db_session.query(models.User).filter(models.User.email == user.email).first()
    if not ex_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    result = utils.verify_hashed_password(plain_password=user.password,hashed_password=ex_user.password)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password didn't match")
    
    return {"status": "OK","code":status.HTTP_200_OK,"token":utils.create_jwt_token(user=ex_user)}
