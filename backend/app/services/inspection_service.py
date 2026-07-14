from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Inspection, School, User
from app.schemas import InspectionCreate, InspectionUpdate


def create_inspection(db: Session, inspection_in: InspectionCreate) -> Inspection:
    """Create a new inspection after verifying school and inspector exist."""
    school = db.query(School).filter(School.id == inspection_in.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    inspector = db.query(User).filter(User.id == inspection_in.inspector_id).first()
    if not inspector:
        raise HTTPException(status_code=404, detail="Inspector not found")

    db_inspection = Inspection(**inspection_in.model_dump())
    db.add(db_inspection)
    db.commit()
    db.refresh(db_inspection)
    return db_inspection


def get_inspection(db: Session, inspection_id: int) -> Inspection:
    """Fetch a single inspection by ID, or raise 404."""
    inspection = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return inspection


def list_inspections(
    db: Session,
    school_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[Inspection]:
    """List inspections with optional filters and pagination."""
    query = db.query(Inspection)
    if school_id:
        query = query.filter(Inspection.school_id == school_id)
    if status_filter:
        query = query.filter(Inspection.status == status_filter)
    return query.offset(skip).limit(limit).all()


def update_inspection(db: Session, inspection_id: int, inspection_in: InspectionUpdate) -> Inspection:
    """Update an inspection's fields, applying only provided values."""
    db_inspection = get_inspection(db, inspection_id)

    update_data = inspection_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_inspection, key, value)

    db.add(db_inspection)
    db.commit()
    db.refresh(db_inspection)
    return db_inspection


def delete_inspection(db: Session, inspection_id: int) -> None:
    """Delete an inspection by ID."""
    db_inspection = get_inspection(db, inspection_id)
    db.delete(db_inspection)
    db.commit()