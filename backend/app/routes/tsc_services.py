from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import TSCService, User, School
from app.schemas import TSCServiceCreate, TSCServiceUpdate, TSCServiceResponse
import uuid

router = APIRouter(prefix="/api/v1/tsc-services", tags=["TSC Services"])

@router.post("/", response_model=TSCServiceResponse)
def create_tsc_service(service: TSCServiceCreate, db: Session = Depends(get_db)):
    """Create a TSC service request."""
    user = db.query(User).filter(User.id == service.requested_by_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    school = db.query(School).filter(School.id == service.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    tsc_ref = f"TSC-{uuid.uuid4().hex[:8].upper()}"
    service_dict = service.dict()
    service_dict["tsc_reference_number"] = tsc_ref
    
    db_service = TSCService(**service_dict)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.get("/{service_id}", response_model=TSCServiceResponse)
def get_tsc_service(service_id: int, db: Session = Depends(get_db)):
    """Get a TSC service request."""
    service = db.query(TSCService).filter(TSCService.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="TSC service not found")
    return service

@router.get("/", response_model=List[TSCServiceResponse])
def list_tsc_services(status: str = None, db: Session = Depends(get_db)):
    """List TSC service requests."""
    query = db.query(TSCService)
    if status:
        query = query.filter(TSCService.status == status)
    return query.all()

@router.patch("/{service_id}", response_model=TSCServiceResponse)
def update_tsc_service(service_id: int, service: TSCServiceUpdate, db: Session = Depends(get_db)):
    """Update a TSC service request."""
    db_service = db.query(TSCService).filter(TSCService.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="TSC service not found")
    
    update_data = service.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_service, key, value)
    
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.delete("/{service_id}")
def delete_tsc_service(service_id: int, db: Session = Depends(get_db)):
    """Delete a TSC service request."""
    service = db.query(TSCService).filter(TSCService.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="TSC service not found")
    
    db.delete(service)
    db.commit()
    return {"message": "TSC service deleted successfully"}
