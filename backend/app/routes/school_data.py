from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import SchoolDataCreate, SchoolDataUpdate, SchoolDataResponse
from app.services import school_data_service

router = APIRouter(prefix="/api/v1/school-data", tags=["School Data Collection"])

@router.post("/", response_model=SchoolDataResponse)
def create_school_data(data: SchoolDataCreate, db: Session = Depends(get_db)):
    return school_data_service.create_school_data(db, data)

@router.get("/{data_id}", response_model=SchoolDataResponse)
def get_school_data(data_id: int, db: Session = Depends(get_db)):
    return school_data_service.get_school_data(db, data_id)

@router.get("/school/{school_id}", response_model=List[SchoolDataResponse])
def get_school_data_by_school(school_id: int, db: Session = Depends(get_db)):
    return school_data_service.get_school_data_by_school(db, school_id)

@router.patch("/{data_id}", response_model=SchoolDataResponse)
def update_school_data(data_id: int, data: SchoolDataUpdate, db: Session = Depends(get_db)):
    return school_data_service.update_school_data(db, data_id, data)

@router.delete("/{data_id}")
def delete_school_data(data_id: int, db: Session = Depends(get_db)):
    school_data_service.delete_school_data(db, data_id)
    return {"message": "School data deleted successfully"}