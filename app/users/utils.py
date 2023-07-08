"""
Authentication utilities:
- includes : 
    -> utitility functions and classess
"""
# go to root directory
import sys
sys.path.append("../../")

import sys
sys.path.append("../../")
import app.server.models as models

from dotenv import load_dotenv,find_dotenv
from passlib.context import CryptContext
from jose import jwt

import os


### FUNCTIONS ###

# get all environment variables needed
load_dotenv(find_dotenv())
secret_key = os.getenv('SECRET_KEY')
algorithm = os.environ.get('ALGORITHM')
scheme1 = os.environ.get('BCRYPT_SCHEM1')
scheme2 = os.environ.get('BCRYPT_SCHEM2')

# create crypt context instance - for encoding
bcrypt_context = CryptContext(schemes=[scheme1, scheme2], deprecated='auto')

# generate hash password
def get_hash_password(plain_password: str) -> str:
    """
    plain password converted to hashed password
    :param: plain_password: string
    :return: hashed_password: string 
    """
    # get hashed password and return
    return bcrypt_context.hash(plain_password)

# verify hashed password
def verify_hashed_password(plain_password: str, hashed_password: str)-> bool:
    """
    verify between hashed password (which is on the database)
    and plain password (which is on the request model).
    :param: plain_password: string
    :param: hashed_password: string
    :return: true(both are same) or false
    """
    return bcrypt_context.verify(plain_password,hashed_password)

# create jwt token
def create_jwt_token(user: models.User) -> str:
    """
    create jwt token 
    :param: user: admin model
    :return: jwt: str
    """
    return jwt.encode({
        "id": user.id,
        "name": user.name,
        "email": user.email,
    },key=secret_key,)