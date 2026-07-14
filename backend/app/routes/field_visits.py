from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import FieldVisitCreate, FieldVisitUpdate, FieldVisitResponse
from app.services import field_visit_service

router = APIRouter(prefix="/api/v1/field-visits", tags=["Field Visits"])

@router.post("/", response_model=FieldVisitResponse)
def create_field_visit(visit: FieldVisitCreate, db: Session = Depends(get_db)):
    return field_visit_service.create_field_visit(db, visit)

@router.get("/{visit_id}", response_model=FieldVisitResponse)
def get_field_visit(visit_id: int, db: Session = Depends(get_db)):
    return field_visit_service.get_field_visit(db, visit_id)

@router.get("/", response_model=List[FieldVisitResponse])
def list_field_visits(
    school_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return field_visit_service.list_field_visits(db, school_id, status, skip, limit)

@router.patch("/{visit_id}", response_model=FieldVisitResponse)
def update_field_visit(visit_id: int, visit: FieldVisitUpdate, db: Session = Depends(get_db)):
    return field_visit_service.update_field_visit(db, visit_id, visit)

@router.delete("/{visit_id}")
def delete_field_visit(visit_id: int, db: Session = Depends(get_db)):
    field_visit_service.delete_field_visit(db, visit_id)
    return {"message": "Field visit deleted successfully"}