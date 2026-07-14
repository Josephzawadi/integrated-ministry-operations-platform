from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import ComplaintCreate, ComplaintUpdate, ComplaintResponse
from app.services import complaint_service

router = APIRouter(prefix="/api/v1/complaints", tags=["Complaints"])

@router.post("/", response_model=ComplaintResponse)
def create_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    return complaint_service.create_complaint(db, complaint)

@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    return complaint_service.get_complaint(db, complaint_id)

@router.get("/", response_model=List[ComplaintResponse])
def list_complaints(
    school_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return complaint_service.list_complaints(db, school_id, status_filter, skip, limit)

@router.patch("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(complaint_id: int, complaint: ComplaintUpdate, db: Session = Depends(get_db)):
    return complaint_service.update_complaint(db, complaint_id, complaint)

@router.delete("/{complaint_id}")
def delete_complaint(complaint_id: int, db: Session = Depends(get_db)):
    complaint_service.delete_complaint(db, complaint_id)
    return {"message": "Complaint deleted successfully"}