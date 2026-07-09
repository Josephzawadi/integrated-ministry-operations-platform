from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.utils.permissions import UserRole

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.SUPPORT_STAFF)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    school = relationship("School", back_populates="principal")
    inspections = relationship("Inspection", back_populates="inspector")
    complaints = relationship("Complaint", back_populates="submitted_by")
    visits = relationship("FieldVisit", back_populates="assigned_to")
    tsc_requests = relationship("TSCService", back_populates="requested_by")

class School(Base):
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    registration_number = Column(String, unique=True, index=True)
    county = Column(String, index=True)
    subcounty = Column(String)
    constituency = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    principal_id = Column(Integer, ForeignKey("users.id"))
    contact_person = Column(String)
    contact_phone = Column(String)
    contact_email = Column(String)
    school_type = Column(String)  # Primary, Secondary, ECDE
    status = Column(String, default="active")  # active, inactive, closed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    principal = relationship("User", back_populates="school")
    inspections = relationship("Inspection", back_populates="school")
    complaints = relationship("Complaint", back_populates="school")
    data_collections = relationship("SchoolData", back_populates="school")
    resources = relationship("ResourceAllocation", back_populates="school")
    visits = relationship("FieldVisit", back_populates="school")

class Inspection(Base):
    __tablename__ = "inspections"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    inspector_id = Column(Integer, ForeignKey("users.id"))
    inspection_date = Column(Date)
    status = Column(String, default="scheduled")  # scheduled, in_progress, completed, cancelled
    focus_areas = Column(Text)  # JSON string
    findings = Column(Text)
    recommendations = Column(Text)
    rating = Column(String)  # Excellent, Good, Satisfactory, Needs Improvement
    compliance_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    school = relationship("School", back_populates="inspections")
    inspector = relationship("User", back_populates="inspections")

class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    submitted_by_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text)
    category = Column(String)  # Academic, Staff, Infrastructure, Management, Other
    severity = Column(String, default="medium")  # low, medium, high, critical
    status = Column(String, default="open")  # open, under_review, resolved, closed
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    resolution_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    school = relationship("School", back_populates="complaints")
    submitted_by = relationship("User", back_populates="complaints", foreign_keys=[submitted_by_id])

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=True)
    filename = Column(String)
    file_path = Column(String)
    document_type = Column(String)  # Inspection Report, Policy, Certificate, etc.
    uploaded_by_id = Column(Integer, ForeignKey("users.id"))
    size = Column(Integer)  # File size in bytes
    mime_type = Column(String)
    extracted_text = Column(Text, nullable=True)  # AI extracted text
    ai_summary = Column(Text, nullable=True)  # AI generated summary
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SchoolData(Base):
    __tablename__ = "school_data"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    collection_year = Column(Integer)
    total_students = Column(Integer)
    total_teachers = Column(Integer)
    pupil_teacher_ratio = Column(Float)
    classrooms = Column(Integer)
    laboratories = Column(Integer)
    library = Column(Boolean)
    computer_lab = Column(Boolean)
    internet_connectivity = Column(Boolean)
    water_supply = Column(Boolean)
    electricity = Column(Boolean)
    sanitation_facilities = Column(Integer)
    infrastructure_notes = Column(Text)
    collected_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    school = relationship("School", back_populates="data_collections")

class ResourceAllocation(Base):
    __tablename__ = "resource_allocations"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    resource_type = Column(String)  # Learning materials, Desks, Chairs, Books, etc.
    quantity_allocated = Column(Integer)
    quantity_delivered = Column(Integer, default=0)
    allocation_date = Column(Date)
    delivery_date = Column(Date, nullable=True)
    allocation_budget = Column(Float)
    status = Column(String, default="pending")  # pending, in_transit, delivered, cancelled
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    school = relationship("School", back_populates="resources")

class FieldVisit(Base):
    __tablename__ = "field_visits"
    
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"))
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    visit_date = Column(Date)
    purpose = Column(String)  # Inspection, Monitoring, Support, Assessment
    objectives = Column(Text)
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    findings = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    duration_hours = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    school = relationship("School", back_populates="visits")
    assigned_to = relationship("User", back_populates="visits")

class TSCService(Base):
    __tablename__ = "tsc_services"
    
    id = Column(Integer, primary_key=True, index=True)
    tsc_reference_number = Column(String, unique=True, index=True)
    service_type = Column(String)  # Teacher Registration, Transfer, Promotion, Discipline
    requested_by_id = Column(Integer, ForeignKey("users.id"))
    school_id = Column(Integer, ForeignKey("schools.id"))
    teacher_name = Column(String)
    teacher_tsc_number = Column(String)
    description = Column(Text)
    status = Column(String, default="submitted")  # submitted, processing, approved, rejected, completed
    submission_date = Column(Date)
    expected_completion = Column(Date)
    actual_completion = Column(Date, nullable=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    requested_by = relationship("User", back_populates="tsc_requests")

class Registry(Base):
    __tablename__ = "registry"
    
    id = Column(Integer, primary_key=True, index=True)
    reference_number = Column(String, unique=True, index=True)
    document_title = Column(String)
    document_type = Column(String)  # Memo, Letter, Report, etc.
    content = Column(Text)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    date_received = Column(Date)
    date_processed = Column(Date, nullable=True)
    status = Column(String, default="pending")  # pending, processing, completed, archived
    remarks = Column(Text)
    file_attachment_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
