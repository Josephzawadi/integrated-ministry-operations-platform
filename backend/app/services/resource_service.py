from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import ResourceAllocation, School
from app.schemas import ResourceAllocationCreate, ResourceAllocationUpdate


def create_resource(db: Session, resource_in: ResourceAllocationCreate) -> ResourceAllocation:
    school = db.query(School).filter(School.id == resource_in.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    db_resource = ResourceAllocation(**resource_in.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


def get_resource(db: Session, resource_id: int) -> ResourceAllocation:
    resource = db.query(ResourceAllocation).filter(ResourceAllocation.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


def get_school_resources(
    db: Session, school_id: int, status: Optional[str] = None
) -> List[ResourceAllocation]:
    query = db.query(ResourceAllocation).filter(ResourceAllocation.school_id == school_id)
    if status:
        query = query.filter(ResourceAllocation.status == status)
    return query.all()


def update_resource(db: Session, resource_id: int, resource_in: ResourceAllocationUpdate) -> ResourceAllocation:
    db_resource = get_resource(db, resource_id)
    update_data = resource_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_resource, key, value)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


def delete_resource(db: Session, resource_id: int) -> None:
    db_resource = get_resource(db, resource_id)
    db.delete(db_resource)
    db.commit()