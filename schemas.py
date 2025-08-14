from pydantic import BaseModel,Field,field_validator

import datetime

import uuid

from typing import Any, Dict, List,Optional,Tuple

import re

class Departments(BaseModel):
    name: str


class ReadDepartments(BaseModel):
    name: str
    class Config:
        from_attributes = True


class Students(BaseModel):
    full_name: str
    email: Optional[str]=None
    gender: Optional[str]=None
    department_id: Optional[int]=None
    password: Optional[str]=None


class ReadStudents(BaseModel):
    full_name: str
    email: Optional[str]=None
    gender: Optional[str]=None
    department_id: Optional[int]=None
    password: Optional[str]=None
    class Config:
        from_attributes = True




class PutDepartmentsDepartmentId(BaseModel):
    department_id: Optional[int]=None
    name: Optional[str]=None

    class Config:
        from_attributes = True



class PostDepartments(BaseModel):
    name: Optional[str]=None

    class Config:
        from_attributes = True



class PostLoginStudent(BaseModel):
    email: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)

    class Config:
        from_attributes = True



class PostStudentsCreate(BaseModel):
    full_name: str = Field(..., max_length=100)
    email: str = Field(..., max_length=100)
    gender: str = Field(..., max_length=100)
    password: Optional[str]=None

    @field_validator('password')
    def validate_password(cls, value: Optional[str]):
        if value is None:
            if True:
                return value
            else:
                raise ValueError("Field 'password' cannot be None")
        # Ensure re is imported in the generated file
        pattern = r'''^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{}|;:'",.<>/?]{8,}$'''
        if isinstance(value, str) and not re.match(pattern, value):
            # Use repr() for the regex pattern in the error for clarity
            raise ValueError(f"Field 'password' does not match regex pattern")
        return value

    class Config:
        from_attributes = True

