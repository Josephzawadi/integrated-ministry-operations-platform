from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import School
from app.schemas import SchoolCreate, SchoolUpdate, SchoolResponse

router = APIRouter(prefix="/api/v1/schools", tags=["Schools"])

@router.post("/", response_model=SchoolResponse)
def create_school(school: SchoolCreate, db: Session = Depends(get_db)):
    """Create a new school."""
    # Check if school with same registration number exists
    existing = db.query(School).filter(School.registration_number == school.registration_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="School with this registration number already exists")
    
    db_school = School(**school.dict())
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school

@router.get("/{school_id}", response_model=SchoolResponse)
def get_school(school_id: int, db: Session = Depends(get_db)):
    """Get a specific school."""
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school

@router.get("/", response_model=List[SchoolResponse])
def list_schools(county: str = None, school_type: str = None, db: Session = Depends(get_db)):
    """List schools with optional filters."""
    query = db.query(School)
    if county:
        query = query.filter(School.county == county)
    if school_type:
        query = query.filter(School.school_type == school_type)
    return query.all()

@router.patch("/{school_id}", response_model=SchoolResponse)
def update_school(school_id: int, school: SchoolUpdate, db: Session = Depends(get_db)):
    """Update a school."""
    db_school = db.query(School).filter(School.id == school_id).first()
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")
    
    update_data = school.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_school, key, value)
    
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school

@router.delete("/{school_id}")
def delete_school(school_id: int, db: Session = Depends(get_db)):
    """Delete a school."""
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    db.delete(school)
    db.commit()
    return {"message": "School deleted successfully"}
