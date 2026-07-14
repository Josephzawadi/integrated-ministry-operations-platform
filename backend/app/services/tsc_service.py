from typing import List, Optional
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import TSCService, User, School
from app.schemas import TSCServiceCreate, TSCServiceUpdate


def create_tsc_service(db: Session, service_in: TSCServiceCreate) -> TSCService:
    user = db.query(User).filter(User.id == service_in.requested_by_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    school = db.query(School).filter(School.id == service_in.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    tsc_ref = f"TSC-{uuid.uuid4().hex[:8].upper()}"
    service_dict = service_in.model_dump()
    service_dict["tsc_reference_number"] = tsc_ref

    db_service = TSCService(**service_dict)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def get_tsc_service(db: Session, service_id: int) -> TSCService:
    service = db.query(TSCService).filter(TSCService.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="TSC service not found")
    return service


def list_tsc_services(
    db: Session, status: Optional[str] = None, skip: int = 0, limit: int = 100
) -> List[TSCService]:
    query = db.query(TSCService)
    if status:
        query = query.filter(TSCService.status == status)
    return query.offset(skip).limit(limit).all()


def update_tsc_service(db: Session, service_id: int, service_in: TSCServiceUpdate) -> TSCService:
    db_service = get_tsc_service(db, service_id)
    update_data = service_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_service, key, value)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def delete_tsc_service(db: Session, service_id: int) -> None:
    db_service = get_tsc_service(db, service_id)
    db.delete(db_service)
    db.commit()