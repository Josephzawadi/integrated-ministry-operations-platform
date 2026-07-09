from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Registry, User
from app.schemas import RegistryCreate, RegistryUpdate, RegistryResponse
import uuid

router = APIRouter(prefix="/api/v1/registry", tags=["Registry Management"])

@router.post("/", response_model=RegistryResponse)
def create_registry(registry: RegistryCreate, db: Session = Depends(get_db)):
    """Create a registry entry."""
    user = db.query(User).filter(User.id == registry.created_by_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    ref_number = f"REG-{uuid.uuid4().hex[:8].upper()}"
    registry_dict = registry.dict()
    registry_dict["reference_number"] = ref_number
    
    db_registry = Registry(**registry_dict)
    db.add(db_registry)
    db.commit()
    db.refresh(db_registry)
    return db_registry

@router.get("/{registry_id}", response_model=RegistryResponse)
def get_registry(registry_id: int, db: Session = Depends(get_db)):
    """Get a registry entry."""
    registry = db.query(Registry).filter(Registry.id == registry_id).first()
    if not registry:
        raise HTTPException(status_code=404, detail="Registry entry not found")
    return registry

@router.get("/", response_model=List[RegistryResponse])
def list_registry(status: str = None, db: Session = Depends(get_db)):
    """List registry entries."""
    query = db.query(Registry)
    if status:
        query = query.filter(Registry.status == status)
    return query.all()

@router.patch("/{registry_id}", response_model=RegistryResponse)
def update_registry(registry_id: int, registry: RegistryUpdate, db: Session = Depends(get_db)):
    """Update a registry entry."""
    db_registry = db.query(Registry).filter(Registry.id == registry_id).first()
    if not db_registry:
        raise HTTPException(status_code=404, detail="Registry entry not found")
    
    update_data = registry.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_registry, key, value)
    
    db.add(db_registry)
    db.commit()
    db.refresh(db_registry)
    return db_registry

@router.delete("/{registry_id}")
def delete_registry(registry_id: int, db: Session = Depends(get_db)):
    """Delete a registry entry."""
    registry = db.query(Registry).filter(Registry.id == registry_id).first()
    if not registry:
        raise HTTPException(status_code=404, detail="Registry entry not found")
    
    db.delete(registry)
    db.commit()
    return {"message": "Registry entry deleted successfully"}
