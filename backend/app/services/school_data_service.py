from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import SchoolData, School
from app.schemas import SchoolDataCreate, SchoolDataUpdate


def create_school_data(db: Session, data_in: SchoolDataCreate) -> SchoolData:
    school = db.query(School).filter(School.id == data_in.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    db_data = SchoolData(**data_in.model_dump())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_school_data(db: Session, data_id: int) -> SchoolData:
    data = db.query(SchoolData).filter(SchoolData.id == data_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="School data not found")
    return data


def get_school_data_by_school(db: Session, school_id: int) -> List[SchoolData]:
    return db.query(SchoolData).filter(SchoolData.school_id == school_id).all()


def update_school_data(db: Session, data_id: int, data_in: SchoolDataUpdate) -> SchoolData:
    db_data = get_school_data(db, data_id)
    update_data = data_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_data, key, value)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def delete_school_data(db: Session, data_id: int) -> None:
    db_data = get_school_data(db, data_id)
    db.delete(db_data)
    db.commit()