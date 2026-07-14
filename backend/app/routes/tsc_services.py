from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import TSCServiceCreate, TSCServiceUpdate, TSCServiceResponse
from app.services import tsc_service

router = APIRouter(prefix="/api/v1/tsc-services", tags=["TSC Services"])

@router.post("/", response_model=TSCServiceResponse)
def create_tsc_service(service: TSCServiceCreate, db: Session = Depends(get_db)):
    return tsc_service.create_tsc_service(db, service)

@router.get("/{service_id}", response_model=TSCServiceResponse)
def get_tsc_service(service_id: int, db: Session = Depends(get_db)):
    return tsc_service.get_tsc_service(db, service_id)

@router.get("/", response_model=List[TSCServiceResponse])
def list_tsc_services(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return tsc_service.list_tsc_services(db, status, skip, limit)

@router.patch("/{service_id}", response_model=TSCServiceResponse)
def update_tsc_service(service_id: int, service: TSCServiceUpdate, db: Session = Depends(get_db)):
    return tsc_service.update_tsc_service(db, service_id, service)

@router.delete("/{service_id}")
def delete_tsc_service(service_id: int, db: Session = Depends(get_db)):
    tsc_service.delete_tsc_service(db, service_id)
    return {"message": "TSC service deleted successfully"}