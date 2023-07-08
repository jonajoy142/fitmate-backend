import sys
sys.path.append("../")
from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.server.database import engine

from app.users.authetication import authRouter
from app.users.biomatrix import bioMetrixRouter

import app.server.models as models

# main router
app = FastAPI(title="FITMATE API", version=0.1)

#create all tables in the database
models.base.metadata.create_all(bind=engine)

# root 
@app.get(path="/",tags=["Root Route"])
def read_root():
    """
    read the root of the api
    :return : status of the api
    """
    return {"status":"OK","message":"Available to integrate"}

# include auth router
app.include_router(router=authRouter,tags=["User Authentication"],prefix='/user')

# include bio matrix router
app.include_router(router=bioMetrixRouter,tags=["User BioMetrix"],prefix='/user/data')