from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ResourceAllocation, School
from app.schemas import ResourceAllocationCreate, ResourceAllocationUpdate, ResourceAllocationResponse

router = APIRouter(prefix="/api/v1/resources", tags=["Resource Distribution"])

@router.post("/", response_model=ResourceAllocationResponse)
def create_resource(resource: ResourceAllocationCreate, db: Session = Depends(get_db)):
    """Create a resource allocation."""
    school = db.query(School).filter(School.id == resource.school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    db_resource = ResourceAllocation(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@router.get("/{resource_id}", response_model=ResourceAllocationResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    """Get a resource allocation."""
    resource = db.query(ResourceAllocation).filter(ResourceAllocation.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.get("/school/{school_id}", response_model=List[ResourceAllocationResponse])
def get_school_resources(school_id: int, status: str = None, db: Session = Depends(get_db)):
    """Get resources for a school."""
    query = db.query(ResourceAllocation).filter(ResourceAllocation.school_id == school_id)
    if status:
        query = query.filter(ResourceAllocation.status == status)
    return query.all()

@router.patch("/{resource_id}", response_model=ResourceAllocationResponse)
def update_resource(resource_id: int, resource: ResourceAllocationUpdate, db: Session = Depends(get_db)):
    """Update a resource allocation."""
    db_resource = db.query(ResourceAllocation).filter(ResourceAllocation.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    update_data = resource.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_resource, key, value)
    
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@router.delete("/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    """Delete a resource allocation."""
    resource = db.query(ResourceAllocation).filter(ResourceAllocation.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    db.delete(resource)
    db.commit()
    return {"message": "Resource deleted successfully"}
