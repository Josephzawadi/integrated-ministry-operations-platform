from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Complaint, School
from app.schemas import ComplaintCreate, ComplaintUpdate


def create_complaint(db: Session, complaint_in: ComplaintCreate) -> Complaint:
    school = db.query(School).filter(School.id == complaint_in.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    db_complaint = Complaint(**complaint_in.model_dump())
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint


def get_complaint(db: Session, complaint_id: int) -> Complaint:
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


def list_complaints(
    db: Session,
    school_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[Complaint]:
    query = db.query(Complaint)
    if school_id:
        query = query.filter(Complaint.school_id == school_id)
    if status_filter:
        query = query.filter(Complaint.status == status_filter)
    return query.offset(skip).limit(limit).all()


def update_complaint(db: Session, complaint_id: int, complaint_in: ComplaintUpdate) -> Complaint:
    db_complaint = get_complaint(db, complaint_id)
    update_data = complaint_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_complaint, key, value)
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint


def delete_complaint(db: Session, complaint_id: int) -> None:
    db_complaint = get_complaint(db, complaint_id)
    db.delete(db_complaint)
    db.commit()