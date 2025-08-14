from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile,Query, Form
from sqlalchemy.orm import Session
from typing import List,Annotated
import service, models, schemas
from fastapi import Query
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/departments/')
async def get_departments(db: Session = Depends(get_db)):
    try:
        return await service.get_departments(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/test')
async def get_test(db: Session = Depends(get_db)):
    try:
        return await service.get_test(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/departments/department_id')
async def get_departments_department_id(department_id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_departments_department_id(db, department_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/departments/department_id/')
async def put_departments_department_id(raw_data: schemas.PutDepartmentsDepartmentId, db: Session = Depends(get_db)):
    try:
        return await service.put_departments_department_id(db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/departments/department_id')
async def delete_departments_department_id(department_id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_departments_department_id(db, department_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/departments/')
async def post_departments(raw_data: schemas.PostDepartments, db: Session = Depends(get_db)):
    try:
        return await service.post_departments(db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/login/student')
async def post_login_student(raw_data: schemas.PostLoginStudent, db: Session = Depends(get_db)):
    try:
        return await service.post_login_student(db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/student/id')
async def get_student_id(id: int, headers: Request, db: Session = Depends(get_db)):
    try:
        return await service.get_student_id(db, id, headers)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/students/create')
async def post_students_create(raw_data: schemas.PostStudentsCreate, db: Session = Depends(get_db)):
    try:
        return await service.post_students_create(db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

