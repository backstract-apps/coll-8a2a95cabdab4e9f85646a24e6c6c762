from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
import datetime
import requests
import math
import random
import asyncio
from pathlib import Path


async def get_departments(db: Session):

    query = db.query(models.Departments)

    departments_all = query.all()
    departments_all = (
        [new_data.to_dict() for new_data in departments_all]
        if departments_all
        else departments_all
    )
    res = {
        "departments_all": departments_all,
    }
    return res


async def get_test(db: Session):

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "value": {},
    }
    return res


async def get_departments_department_id(db: Session, department_id: int):

    query = db.query(models.Departments)
    query = query.filter(and_(models.Departments.department_id == department_id))

    departments_one = query.first()

    departments_one = (
        (
            departments_one.to_dict()
            if hasattr(departments_one, "to_dict")
            else vars(departments_one)
        )
        if departments_one
        else departments_one
    )

    res = {
        "departments_one": departments_one,
    }
    return res


async def put_departments_department_id(
    db: Session, raw_data: schemas.PutDepartmentsDepartmentId
):
    department_id: int = raw_data.department_id
    name: str = raw_data.name

    query = db.query(models.Departments)
    query = query.filter(and_(models.Departments.department_id == department_id))
    departments_edited_record = query.first()

    if departments_edited_record:
        for key, value in {"name": name, "department_id": department_id}.items():
            setattr(departments_edited_record, key, value)

        db.commit()
        db.refresh(departments_edited_record)

        departments_edited_record = (
            departments_edited_record.to_dict()
            if hasattr(departments_edited_record, "to_dict")
            else vars(departments_edited_record)
        )
    res = {
        "departments_edited_record": departments_edited_record,
    }
    return res


async def delete_departments_department_id(db: Session, department_id: int):

    query = db.query(models.Departments)
    query = query.filter(and_(models.Departments.department_id == department_id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        departments_deleted = record_to_delete.to_dict()
    else:
        departments_deleted = record_to_delete
    res = {
        "departments_deleted": departments_deleted,
    }
    return res


async def post_departments(db: Session, raw_data: schemas.PostDepartments):
    name: str = raw_data.name

    record_to_be_added = {"name": name}
    new_departments = models.Departments(**record_to_be_added)
    db.add(new_departments)
    db.commit()
    db.refresh(new_departments)
    departments_inserted_record = new_departments.to_dict()

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "value": {},
    }
    return res


async def post_login_student(db: Session, raw_data: schemas.PostLoginStudent):
    email: str = raw_data.email
    password: str = raw_data.password

    query = db.query(models.Students)
    query = query.filter(
        and_(models.Students.email == email, models.Students.password == password)
    )

    login_record = query.first()

    login_record = (
        (
            login_record.to_dict()
            if hasattr(login_record, "to_dict")
            else vars(login_record)
        )
        if login_record
        else login_record
    )

    try:
        is_exist_login = bool(login_record)
        is_true = True
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    is_As: bool = is_true

    if is_As == is_exist_login:

        bs_jwt_payload = {
            "exp": int(
                (
                    datetime.datetime.utcnow() + datetime.timedelta(seconds=100000)
                ).timestamp()
            ),
            "data": login_record,
        }

        jwt_secret_keys_login1 = jwt.encode(
            bs_jwt_payload,
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30",
            algorithm="HS256",
        )

    else:

        raise HTTPException(status_code=401, detail="user not exist")

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "value": {"jwt_1": "jwt_secret_keys_login1", "login": "login_record"},
        "data": {},
    }
    return res


async def get_student_id(db: Session, id: int, request: Request):
    header_authorization: str = request.headers.get("header-authorization")

    query = db.query(models.Students)
    query = query.filter(and_(models.Students.student_id == id))

    test = query.first()

    test = (
        (test.to_dict() if hasattr(test, "to_dict") else vars(test)) if test else test
    )

    try:
        cxvbxcbc = jwt.decode(
            header_authorization,
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30",
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        cxvbxcbc = "Token has expired."
    except jwt.InvalidTokenError:
        cxvbxcbc = "Invalid token."

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "value": {"dgdfg": "test", "vgvnvb": "cxvbxcbc"},
        "data": {},
    }
    return res


async def post_students_create(db: Session, raw_data: schemas.PostStudentsCreate):
    full_name: str = raw_data.full_name
    email: str = raw_data.email
    gender: str = raw_data.gender
    password: str = raw_data.password

    record_to_be_added = {
        "email": email,
        "gender": gender,
        "password": password,
        "full_name": full_name,
    }
    new_students = models.Students(**record_to_be_added)
    db.add(new_students)
    db.commit()
    db.refresh(new_students)
    add_a_record = new_students.to_dict()

    res = {
        "status": 200,
        "message": "user created successfully",
        "value": {"add_a_record": "add_a_record"},
        "data": {},
    }
    return res
