from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Complaint, School, User
from app.schemas import ComplaintCreate, ComplaintUpdate, ComplaintResponse

router = APIRouter(prefix="/api/v1/complaints", tags=["Complaints"])

@router.post("/", response_model=ComplaintResponse)
def create_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    """Create a new complaint."""
    school = db.query(School).filter(School.id == complaint.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    db_complaint = Complaint(**complaint.dict())
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    """Get a specific complaint."""
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

@router.get("/", response_model=List[ComplaintResponse])
def list_complaints(school_id: int = None, status_filter: str = None, db: Session = Depends(get_db)):
    """List complaints with optional filters."""
    query = db.query(Complaint)
    if school_id:
        query = query.filter(Complaint.school_id == school_id)
    if status_filter:
        query = query.filter(Complaint.status == status_filter)
    return query.all()

@router.patch("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(complaint_id: int, complaint: ComplaintUpdate, db: Session = Depends(get_db)):
    """Update a complaint."""
    db_complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not db_complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    update_data = complaint.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_complaint, key, value)
    
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint

@router.delete("/{complaint_id}")
def delete_complaint(complaint_id: int, db: Session = Depends(get_db)):
    """Delete a complaint."""
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    db.delete(complaint)
    db.commit()
    return {"message": "Complaint deleted successfully"}
