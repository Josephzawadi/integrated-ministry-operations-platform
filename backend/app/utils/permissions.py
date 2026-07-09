from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    INSPECTOR = "inspector"
    SUPPORT_STAFF = "support_staff"
    PRINCIPAL = "principal"
    MINISTRY_OFFICIAL = "ministry_official"
    TSC_OFFICIAL = "tsc_official"
    DATA_ANALYST = "data_analyst"
    VIEWER = "viewer"
