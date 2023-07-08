from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    password: str


class SignInForm(BaseModel):
    email: str
    password: str

class BioMatricData(BaseModel):
    age: int 
    height: float
    weight: float 

class UpdateBioMatricData(BaseModel):
    age: Optional[int] = None
    height: Optional[float] = None
    weight: Optional[float] = None 