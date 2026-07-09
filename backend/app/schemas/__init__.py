from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from app.utils.permissions import UserRole

# ==================== User Schemas ====================
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.SUPPORT_STAFF

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ==================== School Schemas ====================
class SchoolBase(BaseModel):
    name: str
    registration_number: str
    county: str
    subcounty: str
    constituency: str
    school_type: str
    principal_id: Optional[int] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class SchoolCreate(SchoolBase):
    pass

class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    county: Optional[str] = None
    subcounty: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    status: Optional[str] = None

class SchoolResponse(SchoolBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ==================== Inspection Schemas ====================
class InspectionBase(BaseModel):
    school_id: int
    inspection_date: date
    focus_areas: str
    status: str = "scheduled"

class InspectionCreate(InspectionBase):
    inspector_id: int

class InspectionUpdate(BaseModel):
    status: Optional[str] = None
    findings: Optional[str] = None
    recommendations: Optional[str] = None
    rating: Optional[str] = None
    compliance_score: Optional[float] = None

class InspectionResponse(InspectionBase):
    id: int
    inspector_id: int
    findings: Optional[str]
    recommendations: Optional[str]
    rating: Optional[str]
    compliance_score: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ==================== Complaint Schemas ====================
class ComplaintBase(BaseModel):
    school_id: int
    title: str
    description: str
    category: str
    severity: str = "medium"

class ComplaintCreate(ComplaintBase):
    submitted_by_id: int

class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    resolution_notes: Optional[str] = None
    assigned_to_id: Optional[int] = None

class ComplaintResponse(ComplaintBase):
    id: int
    status: str
    submitted_by_id: int
    assigned_to_id: Optional[int]
    resolution_notes: Optional[str]
    created_at: datetime
    resolved_at: Optional[datetime]
    updated_at: datetime

    class Config:
        from_attributes = True

# ==================== Document Schemas ====================
class DocumentBase(BaseModel):
    filename: str
    document_type: str
    mime_type: str

class DocumentCreate(DocumentBase):
    school_id: Optional[int] = None
    uploaded_by_id: int
    size: int
    file_path: str

class DocumentUpdate(BaseModel):
    ai_summary: Optional[str] = None
    extracted_text: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: int
    school_id: Optional[int]
    uploaded_by_id: int
    size: int
    extracted_text: Optional[str]
    ai_summary: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ==================== School Data Schemas ====================
class SchoolDataBase(BaseModel):
    collection_year: int
    total_students: int
    total_teachers: int
    classrooms: int
    laboratories: int

class SchoolDataCreate(SchoolDataBase):
    school_id: int
    pupil_teacher_ratio: Optional[float] = None
    library: bool = False
    computer_lab: bool = False
    internet_connectivity: bool = False
    water_supply: bool = False
    electricity: bool = False
    sanitation_facilities: int = 0
    infrastructure_notes: Optional[str] = None
    collected_by_id: int

class SchoolDataUpdate(BaseModel):
    total_students: Optional[int] = None
    total_teachers: Optional[int] = None
    infrastructure_notes: Optional[str] = None

class SchoolDataResponse(SchoolDataBase):
    id: int
    school_id: int
    pupil_teacher_ratio: Optional[float]
    library: bool
    computer_lab: bool
    internet_connectivity: bool
    water_supply: bool
    electricity: bool
    sanitation_facilities: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ==================== Resource Allocation Schemas ====================
class ResourceAllocationBase(BaseModel):
    resource_type: str
    quantity_allocated: int
    allocation_date: date
    allocation_budget: float

class ResourceAllocationCreate(ResourceAllocationBase):
    school_id: int

class ResourceAllocationUpdate(BaseModel):
    quantity_delivered: Optional[int] = None
    delivery_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class ResourceAllocationResponse(ResourceAllocationBase):
    id: int
    school_id: int
    quantity_delivered: int
    delivery_date: Optional[date]
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ==================== Field Visit Schemas ====================
class FieldVisitBase(BaseModel):
    school_id: int
    visit_date: date
    purpose: str
    objectives: str

class FieldVisitCreate(FieldVisitBase):
    assigned_to_id: int

class FieldVisitUpdate(BaseModel):
    status: Optional[str] = None
    findings: Optional[str] = None
    recommendations: Optional[str] = None
    duration_hours: Optional[float] = None

class FieldVisitResponse(FieldVisitBase):
    id: int
    assigned_to_id: int
    status: str
    findings: Optional[str]
    recommendations: Optional[str]
    duration_hours: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ==================== TSC Service Schemas ====================
class TSCServiceBase(BaseModel):
    service_type: str
    school_id: int
    teacher_name: str
    teacher_tsc_number: str
    description: str
    submission_date: date
    expected_completion: date

class TSCServiceCreate(TSCServiceBase):
    requested_by_id: int

class TSCServiceUpdate(BaseModel):
    status: Optional[str] = None
    actual_completion: Optional[date] = None
    notes: Optional[str] = None

class TSCServiceResponse(TSCServiceBase):
    id: int
    tsc_reference_number: str
    requested_by_id: int
    status: str
    actual_completion: Optional[date]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ==================== Registry Schemas ====================
class RegistryBase(BaseModel):
    document_title: str
    document_type: str
    content: str
    date_received: date

class RegistryCreate(RegistryBase):
    created_by_id: int
    school_id: Optional[int] = None
    file_attachment_id: Optional[int] = None

class RegistryUpdate(BaseModel):
    status: Optional[str] = None
    date_processed: Optional[date] = None
    remarks: Optional[str] = None

class RegistryResponse(RegistryBase):
    id: int
    reference_number: str
    created_by_id: int
    school_id: Optional[int]
    status: str
    date_processed: Optional[date]
    remarks: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ==================== Authentication Schemas ====================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: UserResponse

# ==================== Generic Response Schemas ====================
class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int

class MessageResponse(BaseModel):
    message: str
    success: bool
