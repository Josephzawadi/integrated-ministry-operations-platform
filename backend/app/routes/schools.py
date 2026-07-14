from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import SchoolCreate, SchoolUpdate, SchoolResponse
from app.services import school_service

router = APIRouter(prefix="/api/v1/schools", tags=["Schools"])

@router.post("/", response_model=SchoolResponse)
def create_school(school: SchoolCreate, db: Session = Depends(get_db)):
    """Create a new school."""
    return school_service.create_school(db, school)

@router.get("/{school_id}", response_model=SchoolResponse)
def get_school(school_id: int, db: Session = Depends(get_db)):
    """Get a specific school."""
    return school_service.get_school(db, school_id)

@router.get("/", response_model=List[SchoolResponse])
def list_schools(
    county: Optional[str] = None,
    school_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List schools with optional filters and pagination."""
    return school_service.list_schools(db, county, school_type, skip, limit)

@router.patch("/{school_id}", response_model=SchoolResponse)
def update_school(school_id: int, school: SchoolUpdate, db: Session = Depends(get_db)):
    """Update a school."""
    return school_service.update_school(db, school_id, school)

@router.delete("/{school_id}")
def delete_school(school_id: int, db: Session = Depends(get_db)):
    """Delete a school."""
    school_service.delete_school(db, school_id)
    return {"message": "School deleted successfully"}