from typing import List, Optional
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Registry, User
from app.schemas import RegistryCreate, RegistryUpdate


def create_registry(db: Session, registry_in: RegistryCreate) -> Registry:
    user = db.query(User).filter(User.id == registry_in.created_by_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ref_number = f"REG-{uuid.uuid4().hex[:8].upper()}"
    registry_dict = registry_in.model_dump()
    registry_dict["reference_number"] = ref_number

    db_registry = Registry(**registry_dict)
    db.add(db_registry)
    db.commit()
    db.refresh(db_registry)
    return db_registry


def get_registry(db: Session, registry_id: int) -> Registry:
    registry = db.query(Registry).filter(Registry.id == registry_id).first()
    if not registry:
        raise HTTPException(status_code=404, detail="Registry entry not found")
    return registry


def list_registry(
    db: Session, status: Optional[str] = None, skip: int = 0, limit: int = 100
) -> List[Registry]:
    query = db.query(Registry)
    if status:
        query = query.filter(Registry.status == status)
    return query.offset(skip).limit(limit).all()


def update_registry(db: Session, registry_id: int, registry_in: RegistryUpdate) -> Registry:
    db_registry = get_registry(db, registry_id)
    update_data = registry_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_registry, key, value)
    db.add(db_registry)
    db.commit()
    db.refresh(db_registry)
    return db_registry


def delete_registry(db: Session, registry_id: int) -> None:
    db_registry = get_registry(db, registry_id)
    db.delete(db_registry)
    db.commit()