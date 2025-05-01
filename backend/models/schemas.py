from pydantic import BaseModel, EmailStr, constr
from datetime import datetime

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=8)

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    cash: float
    registration_date: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username_or_email: str
    password: constr(min_length=8)