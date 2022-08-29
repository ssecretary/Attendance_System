import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class Student(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    days: int = 1
    is_active: bool = False
    created_date = datetime.datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "email": "admin123@gmail.com",
                "password": "admin",
                "days": 1,
                "is_active": False,
                "created_date": datetime.datetime.now()
            }
        }


class UpdateStudentModel(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    days: Optional[int]
    is_active: Optional[bool]
    created_date = datetime.datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "email": "admin123",
                "password": "admin",
                "days": 1,
                "is_active": "False",
                "created_date": datetime.datetime.now()
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
