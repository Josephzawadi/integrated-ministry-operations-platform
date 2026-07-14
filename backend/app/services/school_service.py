from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import School
from app.schemas import SchoolCreate, SchoolUpdate


def create_school(db: Session, school_in: SchoolCreate) -> School:
    """Create a new school, enforcing unique registration number."""
    existing = db.query(School).filter(
        School.registration_number == school_in.registration_number
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="School with this registration number already exists",
        )

    db_school = School(**school_in.model_dump())
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school


def get_school(db: Session, school_id: int) -> School:
    """Fetch a single school by ID, or raise 404."""
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


def list_schools(
    db: Session,
    county: Optional[str] = None,
    school_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[School]:
    """List schools with optional filters and pagination."""
    query = db.query(School)
    if county:
        query = query.filter(School.county == county)
    if school_type:
        query = query.filter(School.school_type == school_type)
    return query.offset(skip).limit(limit).all()


def update_school(db: Session, school_id: int, school_in: SchoolUpdate) -> School:
    """Update a school's fields, applying only provided values."""
    db_school = get_school(db, school_id)

    update_data = school_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_school, key, value)

    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school


def delete_school(db: Session, school_id: int) -> None:
    """Delete a school by ID."""
    db_school = get_school(db, school_id)
    db.delete(db_school)
    db.commit()