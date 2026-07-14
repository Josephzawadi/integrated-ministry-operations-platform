from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import FieldVisit, School, User
from app.schemas import FieldVisitCreate, FieldVisitUpdate


def create_field_visit(db: Session, visit_in: FieldVisitCreate) -> FieldVisit:
    school = db.query(School).filter(School.id == visit_in.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    user = db.query(User).filter(User.id == visit_in.assigned_to_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_visit = FieldVisit(**visit_in.model_dump())
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit


def get_field_visit(db: Session, visit_id: int) -> FieldVisit:
    visit = db.query(FieldVisit).filter(FieldVisit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Field visit not found")
    return visit


def list_field_visits(
    db: Session,
    school_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[FieldVisit]:
    query = db.query(FieldVisit)
    if school_id:
        query = query.filter(FieldVisit.school_id == school_id)
    if status:
        query = query.filter(FieldVisit.status == status)
    return query.offset(skip).limit(limit).all()


def update_field_visit(db: Session, visit_id: int, visit_in: FieldVisitUpdate) -> FieldVisit:
    db_visit = get_field_visit(db, visit_id)
    update_data = visit_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_visit, key, value)
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit


def delete_field_visit(db: Session, visit_id: int) -> None:
    db_visit = get_field_visit(db, visit_id)
    db.delete(db_visit)
    db.commit()