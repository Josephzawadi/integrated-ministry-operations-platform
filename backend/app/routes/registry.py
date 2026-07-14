from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import RegistryCreate, RegistryUpdate, RegistryResponse
from app.services import registry_service

router = APIRouter(prefix="/api/v1/registry", tags=["Registry Management"])

@router.post("/", response_model=RegistryResponse)
def create_registry(registry: RegistryCreate, db: Session = Depends(get_db)):
    return registry_service.create_registry(db, registry)

@router.get("/{registry_id}", response_model=RegistryResponse)
def get_registry(registry_id: int, db: Session = Depends(get_db)):
    return registry_service.get_registry(db, registry_id)

@router.get("/", response_model=List[RegistryResponse])
def list_registry(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return registry_service.list_registry(db, status, skip, limit)

@router.patch("/{registry_id}", response_model=RegistryResponse)
def update_registry(registry_id: int, registry: RegistryUpdate, db: Session = Depends(get_db)):
    return registry_service.update_registry(db, registry_id, registry)

@router.delete("/{registry_id}")
def delete_registry(registry_id: int, db: Session = Depends(get_db)):
    registry_service.delete_registry(db, registry_id)
    return {"message": "Registry entry deleted successfully"}