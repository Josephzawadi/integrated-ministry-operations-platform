from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SchoolData, School
from app.schemas import SchoolDataCreate, SchoolDataUpdate, SchoolDataResponse

router = APIRouter(prefix="/api/v1/school-data", tags=["School Data Collection"])

@router.post("/", response_model=SchoolDataResponse)
def create_school_data(data: SchoolDataCreate, db: Session = Depends(get_db)):
    """Create school data collection record."""
    school = db.query(School).filter(School.id == data.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    db_data = SchoolData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@router.get("/{data_id}", response_model=SchoolDataResponse)
def get_school_data(data_id: int, db: Session = Depends(get_db)):
    """Get school data record."""
    data = db.query(SchoolData).filter(SchoolData.id == data_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="School data not found")
    return data

@router.get("/school/{school_id}", response_model=List[SchoolDataResponse])
def get_school_data_by_school(school_id: int, db: Session = Depends(get_db)):
    """Get all data records for a school."""
    return db.query(SchoolData).filter(SchoolData.school_id == school_id).all()

@router.patch("/{data_id}", response_model=SchoolDataResponse)
def update_school_data(data_id: int, data: SchoolDataUpdate, db: Session = Depends(get_db)):
    """Update school data record."""
    db_data = db.query(SchoolData).filter(SchoolData.id == data_id).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="School data not found")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_data, key, value)
    
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@router.delete("/{data_id}")
def delete_school_data(data_id: int, db: Session = Depends(get_db)):
    """Delete school data record."""
    data = db.query(SchoolData).filter(SchoolData.id == data_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="School data not found")
    
    db.delete(data)
    db.commit()
    return {"message": "School data deleted successfully"}
