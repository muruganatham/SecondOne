"""
User-related Enums - CORRECTED WITH ACTUAL ROLE NAMES
100% accurate data from database + CORRECT role names from user
"""

from enum import IntEnum


class UserRole(IntEnum):
    """
    User roles in the system - CORRECT MAPPINGS
    
    Distribution in database (6,691 total users):
    - SUPER_ADMIN (1): 3 users (0.04%)
    - ADMIN (2): 6 users (0.09%)
    - COLLEGE_ADMIN (3): 2 users (0.03%)
    - STAFF (4): 41 users (0.61%)
    - TRAINER (5): 37 users (0.55%)
    - CONTENT (6): 16 users (0.24%)
    - STUDENT (7): 6,586 users (98.43%)
    """
    SUPER_ADMIN = 1      # Super Admin (3 users - 0.04%)
    ADMIN = 2            # Admin (6 users - 0.09%)
    COLLEGE_ADMIN = 3    # College Admin (2 users - 0.03%)
    STAFF = 4            # Staff (41 users - 0.61%)
    TRAINER = 5          # Trainer (37 users - 0.55%)
    CONTENT = 6          # Content (16 users - 0.24%)
    STUDENT = 7          # Student (6,586 users - 98.43%)
    
    @classmethod
    def is_admin(cls, role_value: int) -> bool:
        """Check if role is any admin type"""
        return role_value in [cls.SUPER_ADMIN, cls.ADMIN, cls.COLLEGE_ADMIN]
    
    @classmethod
    def is_staff(cls, role_value: int) -> bool:
        """Check if role is staff or trainer"""
        return role_value in [cls.STAFF, cls.TRAINER, cls.CONTENT]
    
    @classmethod
    def is_student(cls, role_value: int) -> bool:
        """Check if role is student"""
        return role_value == cls.STUDENT
    
    @classmethod
    def get_display_name(cls, role_value: int) -> str:
        """Get human-readable role name"""
        names = {
            cls.SUPER_ADMIN: "Super Admin",
            cls.ADMIN: "Admin",
            cls.COLLEGE_ADMIN: "College Admin",
            cls.STAFF: "Staff",
            cls.TRAINER: "Trainer",
            cls.CONTENT: "Content",
            cls.STUDENT: "Student"
        }
        return names.get(role_value, f"Unknown Role ({role_value})")


class UserGender(IntEnum):
    """
    User gender - CORRECT MAPPINGS
    
    Distribution in database (3,602 users with gender set):
    - NOT_SPECIFIED (0): 217 users (6.02%)
    - MALE (1): 2,088 users (57.97%)
    - FEMALE (2): 1,290 users (35.81%)
    - OTHERS (3): 7 users (0.19%)
    """
    NOT_SPECIFIED = 0
    MALE = 1
    FEMALE = 2
    OTHERS = 3
    
    @classmethod
    def get_display_name(cls, gender_value: int) -> str:
        """Get human-readable gender name"""
        names = {
            cls.NOT_SPECIFIED: "Not Specified",
            cls.MALE: "Male",
            cls.FEMALE: "Female",
            cls.OTHERS: "Others"
        }
        return names.get(gender_value, f"Unknown ({gender_value})")


class UserStatus(IntEnum):
    """
    User account status
    
    Distribution in database (6,691 total users):
    - DELETED (0): 10 users (0.15%)
    - ACTIVE (1): 4,115 users (61.50%)
    - INACTIVE (2): 2,566 users (38.35%)
    """
    DELETED = 0      # Deleted/Banned account
    ACTIVE = 1       # Active account
    INACTIVE = 2     # Inactive/Suspended account
    
    @classmethod
    def is_active(cls, status_value: int) -> bool:
        """Check if user is active"""
        return status_value == cls.ACTIVE
    
    @classmethod
    def get_display_name(cls, status_value: int) -> str:
        """Get human-readable status name"""
        names = {
            cls.DELETED: "Deleted",
            cls.ACTIVE: "Active",
            cls.INACTIVE: "Inactive"
        }
        return names.get(status_value, f"Unknown ({status_value})")


# Helper functions
def get_role_permissions(role: UserRole) -> dict:
    """Get permission set for a role"""
    permissions = {
        UserRole.SUPER_ADMIN: {
            'can_manage_users': True,
            'can_manage_colleges': True,
            'can_manage_courses': True,
            'can_view_analytics': True,
            'can_manage_system': True,
            'can_manage_content': True,
        },
        UserRole.ADMIN: {
            'can_manage_users': True,
            'can_manage_colleges': True,
            'can_manage_courses': True,
            'can_view_analytics': True,
            'can_manage_system': False,
            'can_manage_content': True,
        },
        UserRole.COLLEGE_ADMIN: {
            'can_manage_users': True,
            'can_manage_colleges': False,
            'can_manage_courses': True,
            'can_view_analytics': True,
            'can_manage_system': False,
            'can_manage_content': False,
        },
        UserRole.STAFF: {
            'can_manage_users': False,
            'can_manage_colleges': False,
            'can_manage_courses': True,
            'can_view_analytics': True,
            'can_manage_system': False,
            'can_manage_content': False,
        },
        UserRole.TRAINER: {
            'can_manage_users': False,
            'can_manage_colleges': False,
            'can_manage_courses': True,
            'can_view_analytics': True,
            'can_manage_system': False,
            'can_manage_content': True,
        },
        UserRole.CONTENT: {
            'can_manage_users': False,
            'can_manage_colleges': False,
            'can_manage_courses': False,
            'can_view_analytics': False,
            'can_manage_system': False,
            'can_manage_content': True,
        },
        UserRole.STUDENT: {
            'can_manage_users': False,
            'can_manage_colleges': False,
            'can_manage_courses': False,
            'can_view_analytics': False,
            'can_manage_system': False,
            'can_manage_content': False,
        },
    }
    return permissions.get(role, {})
