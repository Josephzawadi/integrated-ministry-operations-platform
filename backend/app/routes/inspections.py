from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas import InspectionCreate, InspectionUpdate, InspectionResponse
from app.services import inspection_service

router = APIRouter(prefix="/api/v1/inspections", tags=["Inspections"])

@router.post("/", response_model=InspectionResponse)
def create_inspection(inspection: InspectionCreate, db: Session = Depends(get_db)):
    """Create a new school inspection."""
    return inspection_service.create_inspection(db, inspection)

@router.get("/{inspection_id}", response_model=InspectionResponse)
def get_inspection(inspection_id: int, db: Session = Depends(get_db)):
    """Get a specific inspection by ID."""
    return inspection_service.get_inspection(db, inspection_id)

@router.get("/", response_model=List[InspectionResponse])
def list_inspections(
    school_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List inspections with optional filters and pagination."""
    return inspection_service.list_inspections(db, school_id, status_filter, skip, limit)

@router.patch("/{inspection_id}", response_model=InspectionResponse)
def update_inspection(inspection_id: int, inspection: InspectionUpdate, db: Session = Depends(get_db)):
    """Update an inspection."""
    return inspection_service.update_inspection(db, inspection_id, inspection)

@router.delete("/{inspection_id}")
def delete_inspection(inspection_id: int, db: Session = Depends(get_db)):
    """Delete an inspection."""
    inspection_service.delete_inspection(db, inspection_id)
    return {"message": "Inspection deleted successfully"}