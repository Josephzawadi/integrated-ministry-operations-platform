from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Inspection, School
from app.schemas import InspectionCreate, InspectionUpdate, InspectionResponse
from datetime import date

router = APIRouter(prefix="/api/v1/inspections", tags=["Inspections"])

@router.post("/", response_model=InspectionResponse)
def create_inspection(inspection: InspectionCreate, db: Session = Depends(get_db)):
    """Create a new school inspection."""
    # Verify school exists
    school = db.query(School).filter(School.id == inspection.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Verify inspector exists
    inspector = db.query(User).filter(User.id == inspection.inspector_id).first()
    if not inspector:
        raise HTTPException(status_code=404, detail="Inspector not found")
    
    db_inspection = Inspection(**inspection.dict())
    db.add(db_inspection)
    db.commit()
    db.refresh(db_inspection)
    return db_inspection

@router.get("/{inspection_id}", response_model=InspectionResponse)
def get_inspection(inspection_id: int, db: Session = Depends(get_db)):
    """Get a specific inspection by ID."""
    inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return inspection

@router.get("/", response_model=List[InspectionResponse])
def list_inspections(school_id: int = None, status_filter: str = None, db: Session = Depends(get_db)):
    """List inspections with optional filters."""
    query = db.query(Inspection)
    if school_id:
        query = query.filter(Inspection.school_id == school_id)
    if status_filter:
        query = query.filter(Inspection.status == status_filter)
    return query.all()

@router.patch("/{inspection_id}", response_model=InspectionResponse)
def update_inspection(inspection_id: int, inspection: InspectionUpdate, db: Session = Depends(get_db)):
    """Update an inspection."""
    db_inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not db_inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    
    update_data = inspection.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_inspection, key, value)
    
    db.add(db_inspection)
    db.commit()
    db.refresh(db_inspection)
    return db_inspection

@router.delete("/{inspection_id}")
def delete_inspection(inspection_id: int, db: Session = Depends(get_db)):
    """Delete an inspection."""
    inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    
    db.delete(inspection)
    db.commit()
    return {"message": "Inspection deleted successfully"}
