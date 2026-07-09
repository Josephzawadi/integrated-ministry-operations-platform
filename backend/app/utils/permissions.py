from enum import Enum

class UserRole(str, Enum):
    """User roles in the system."""
    DIRECTOR = "director"
    ADMIN = "admin"
    INSPECTOR = "inspector"
    DATA_OFFICER = "data_officer"
    TSC_OFFICER = "tsc_officer"
    SCHOOL_PRINCIPAL = "school_principal"
    SUPPORT_STAFF = "support_staff"

class Permission(str, Enum):
    """System permissions."""
    # User management
    CREATE_USER = "create_user"
    READ_USER = "read_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    
    # School inspection
    CREATE_INSPECTION = "create_inspection"
    READ_INSPECTION = "read_inspection"
    UPDATE_INSPECTION = "update_inspection"
    DELETE_INSPECTION = "delete_inspection"
    
    # Complaints & Feedback
    CREATE_COMPLAINT = "create_complaint"
    READ_COMPLAINT = "read_complaint"
    UPDATE_COMPLAINT = "update_complaint"
    DELETE_COMPLAINT = "delete_complaint"
    
    # Documents
    CREATE_DOCUMENT = "create_document"
    READ_DOCUMENT = "read_document"
    UPDATE_DOCUMENT = "update_document"
    DELETE_DOCUMENT = "delete_document"
    
    # School Data
    CREATE_SCHOOL = "create_school"
    READ_SCHOOL = "read_school"
    UPDATE_SCHOOL = "update_school"
    DELETE_SCHOOL = "delete_school"
    
    # Resources
    CREATE_RESOURCE = "create_resource"
    READ_RESOURCE = "read_resource"
    UPDATE_RESOURCE = "update_resource"
    DELETE_RESOURCE = "delete_resource"
    
    # Field Visits
    CREATE_VISIT = "create_visit"
    READ_VISIT = "read_visit"
    UPDATE_VISIT = "update_visit"
    DELETE_VISIT = "delete_visit"
    
    # TSC Services
    CREATE_TSC = "create_tsc"
    READ_TSC = "read_tsc"
    UPDATE_TSC = "update_tsc"
    DELETE_TSC = "delete_tsc"
    
    # Registry
    CREATE_REGISTRY = "create_registry"
    READ_REGISTRY = "read_registry"
    UPDATE_REGISTRY = "update_registry"
    DELETE_REGISTRY = "delete_registry"

# Role-based permission mapping
ROLE_PERMISSIONS: dict = {
    UserRole.DIRECTOR: [
        # Full access to all permissions
        perm for perm in Permission
    ],
    UserRole.ADMIN: [
        # Administrative permissions
        Permission.READ_USER,
        Permission.UPDATE_USER,
        Permission.READ_INSPECTION,
        Permission.READ_COMPLAINT,
        Permission.READ_DOCUMENT,
        Permission.READ_SCHOOL,
        Permission.CREATE_SCHOOL,
        Permission.UPDATE_SCHOOL,
        Permission.READ_RESOURCE,
        Permission.CREATE_RESOURCE,
        Permission.UPDATE_RESOURCE,
        Permission.READ_VISIT,
        Permission.READ_TSC,
        Permission.READ_REGISTRY,
    ],
    UserRole.INSPECTOR: [
        # Inspection permissions
        Permission.CREATE_INSPECTION,
        Permission.READ_INSPECTION,
        Permission.UPDATE_INSPECTION,
        Permission.READ_SCHOOL,
        Permission.READ_COMPLAINT,
        Permission.CREATE_VISIT,
        Permission.READ_VISIT,
        Permission.UPDATE_VISIT,
    ],
    UserRole.DATA_OFFICER: [
        # Data collection permissions
        Permission.READ_SCHOOL,
        Permission.CREATE_SCHOOL,
        Permission.UPDATE_SCHOOL,
        Permission.READ_DOCUMENT,
        Permission.CREATE_DOCUMENT,
        Permission.UPDATE_DOCUMENT,
        Permission.READ_RESOURCE,
        Permission.CREATE_RESOURCE,
    ],
    UserRole.TSC_OFFICER: [
        # TSC permissions
        Permission.READ_TSC,
        Permission.CREATE_TSC,
        Permission.UPDATE_TSC,
        Permission.READ_SCHOOL,
    ],
    UserRole.SCHOOL_PRINCIPAL: [
        # Limited school permissions
        Permission.READ_SCHOOL,
        Permission.READ_COMPLAINT,
        Permission.CREATE_COMPLAINT,
        Permission.READ_VISIT,
        Permission.READ_RESOURCE,
    ],
    UserRole.SUPPORT_STAFF: [
        # Registry and document permissions
        Permission.READ_REGISTRY,
        Permission.CREATE_REGISTRY,
        Permission.UPDATE_REGISTRY,
        Permission.READ_DOCUMENT,
        Permission.CREATE_DOCUMENT,
        Permission.UPDATE_DOCUMENT,
    ],
}
