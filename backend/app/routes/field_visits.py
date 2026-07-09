from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import FieldVisit, School, User
from app.schemas import FieldVisitCreate, FieldVisitUpdate, FieldVisitResponse

router = APIRouter(prefix="/api/v1/field-visits", tags=["Field Visits"])

@router.post("/", response_model=FieldVisitResponse)
def create_field_visit(visit: FieldVisitCreate, db: Session = Depends(get_db)):
    """Create a field visit."""
    school = db.query(School).filter(School.id == visit.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    user = db.query(User).filter(User.id == visit.assigned_to_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_visit = FieldVisit(**visit.dict())
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit

@router.get("/{visit_id}", response_model=FieldVisitResponse)
def get_field_visit(visit_id: int, db: Session = Depends(get_db)):
    """Get a field visit."""
    visit = db.query(FieldVisit).filter(FieldVisit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Field visit not found")
    return visit

@router.get("/", response_model=List[FieldVisitResponse])
def list_field_visits(school_id: int = None, status: str = None, db: Session = Depends(get_db)):
    """List field visits."""
    query = db.query(FieldVisit)
    if school_id:
        query = query.filter(FieldVisit.school_id == school_id)
    if status:
        query = query.filter(FieldVisit.status == status)
    return query.all()

@router.patch("/{visit_id}", response_model=FieldVisitResponse)
def update_field_visit(visit_id: int, visit: FieldVisitUpdate, db: Session = Depends(get_db)):
    """Update a field visit."""
    db_visit = db.query(FieldVisit).filter(FieldVisit.id == visit_id).first()
    if not db_visit:
        raise HTTPException(status_code=404, detail="Field visit not found")
    
    update_data = visit.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_visit, key, value)
    
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit

@router.delete("/{visit_id}")
def delete_field_visit(visit_id: int, db: Session = Depends(get_db)):
    """Delete a field visit."""
    visit = db.query(FieldVisit).filter(FieldVisit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Field visit not found")
    
    db.delete(visit)
    db.commit()
    return {"message": "Field visit deleted successfully"}
