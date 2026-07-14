from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import ResourceAllocationCreate, ResourceAllocationUpdate, ResourceAllocationResponse
from app.services import resource_service

router = APIRouter(prefix="/api/v1/resources", tags=["Resource Distribution"])

@router.post("/", response_model=ResourceAllocationResponse)
def create_resource(resource: ResourceAllocationCreate, db: Session = Depends(get_db)):
    return resource_service.create_resource(db, resource)

@router.get("/{resource_id}", response_model=ResourceAllocationResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    return resource_service.get_resource(db, resource_id)

@router.get("/school/{school_id}", response_model=List[ResourceAllocationResponse])
def get_school_resources(school_id: int, status: Optional[str] = None, db: Session = Depends(get_db)):
    return resource_service.get_school_resources(db, school_id, status)

@router.patch("/{resource_id}", response_model=ResourceAllocationResponse)
def update_resource(resource_id: int, resource: ResourceAllocationUpdate, db: Session = Depends(get_db)):
    return resource_service.update_resource(db, resource_id, resource)

@router.delete("/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource_service.delete_resource(db, resource_id)
    return {"message": "Resource deleted successfully"}