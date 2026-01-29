"""
Database Enums - Defined from Manual User Input (100% Accurate)
"""
from enum import IntEnum
from typing import Dict, Any

# Helper to get display names
def get_enum_display(enum_class, value):
    try:
        return enum_class(value).name.replace("_", " ").title()
    except ValueError:
        return f"Unknown ({value})"


# Enums for table: 2025_submission_tracks
class SubmissionTracks2025Mode(IntEnum):
    """Enum for 2025_submission_tracks.mode"""
    MCQ = 1
    CODING = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "mcq",
            2: "coding",
        }
        return labels.get(value, "Unknown")


class SubmissionTracks2025Type(IntEnum):
    """Enum for 2025_submission_tracks.type"""
    PREPARE = 1
    ASSESSMENT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "prepare",
            2: "assessment",
        }
        return labels.get(value, "Unknown")


class SubmissionTracks2025Period(IntEnum):
    """Enum for 2025_submission_tracks.period"""
    MONTH = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "month",
        }
        return labels.get(value, "Unknown")


# Enums for table: 2026_submission_tracks
class SubmissionTracks2026Mode(IntEnum):
    """Enum for 2026_submission_tracks.mode"""
    MCQ_AND_FILLUPS = 1
    CODING = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "Mcq & Fillups",
            2: "Coding",
        }
        return labels.get(value, "Unknown")


class SubmissionTracks2026Type(IntEnum):
    """Enum for 2026_submission_tracks.type"""
    PREPARE = 1
    ASSESSMENT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "Prepare",
            2: "Assessment",
        }
        return labels.get(value, "Unknown")


class SubmissionTracks2026Period(IntEnum):
    """Enum for 2026_submission_tracks.period"""
    MONTH = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "month",
        }
        return labels.get(value, "Unknown")


# Enums for table: MCET_2025_2_coding_result
class McetTopicType(IntEnum):
    """Enum for MCET_2025_2_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class McetType(IntEnum):
    """Enum for MCET_2025_2_coding_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class McetSolveStatus(IntEnum):
    """Enum for MCET_2025_2_coding_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class McetStatus(IntEnum):
    """Enum for MCET_2025_2_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: MCET_2025_2_test_data
class McetTopicType(IntEnum):
    """Enum for MCET_2025_2_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class McetStatus(IntEnum):
    """Enum for MCET_2025_2_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: MCET_2026_1_coding_result
class McetTopicType(IntEnum):
    """Enum for MCET_2026_1_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class McetType(IntEnum):
    """Enum for MCET_2026_1_coding_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class McetSolveStatus(IntEnum):
    """Enum for MCET_2026_1_coding_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class McetStatus(IntEnum):
    """Enum for MCET_2026_1_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: MCET_2026_1_mcq_result
class McetTopicType(IntEnum):
    """Enum for MCET_2026_1_mcq_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class McetType(IntEnum):
    """Enum for MCET_2026_1_mcq_result.type"""
    FILLUPS = 1
    MCQ = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "fillups",
            2: "mcq",
        }
        return labels.get(value, "Unknown")


class McetSolveStatus(IntEnum):
    """Enum for MCET_2026_1_mcq_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class McetStatus(IntEnum):
    """Enum for MCET_2026_1_mcq_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: MCET_2026_1_test_data
class McetTopicType(IntEnum):
    """Enum for MCET_2026_1_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class McetStatus(IntEnum):
    """Enum for MCET_2026_1_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: academic_qb_mcqs
class AcademicQbMcqsQuestionCategory(IntEnum):
    """Enum for academic_qb_mcqs.question_category"""
    FILLUPS = 1
    MCQ = 2
    VERBALS = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "fillups",
            2: "mcq",
            3: "verbals",
        }
        return labels.get(value, "Unknown")


class AcademicQbMcqsQuestionType(IntEnum):
    """Enum for academic_qb_mcqs.question_type"""
    ANSWER_SHUFFLE = 1
    MULTI_OPTIONS = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "answer shuffle",
            2: "multi options",
        }
        return labels.get(value, "Unknown")


class AcademicQbMcqsStatus(IntEnum):
    """Enum for academic_qb_mcqs.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: academic_qb_projects
class AcademicQbProjectsQuestionType(IntEnum):
    """Enum for academic_qb_projects.question_type"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: academic_study_material_banks
class AcademicStudyMaterialBanksStatus(IntEnum):
    """Enum for academic_study_material_banks.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: admin_coding_result
class AdminTopicType(IntEnum):
    """Enum for admin_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class AdminSolveStatus(IntEnum):
    """Enum for admin_coding_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class AdminStatus(IntEnum):
    """Enum for admin_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: admin_mcq_result
class AdminTopicType(IntEnum):
    """Enum for admin_mcq_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class AdminType(IntEnum):
    """Enum for admin_mcq_result.type"""
    FILLUPS = 1
    MCQ = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "fillups",
            2: "mcq",
        }
        return labels.get(value, "Unknown")


class AdminSolveStatus(IntEnum):
    """Enum for admin_mcq_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class AdminStatus(IntEnum):
    """Enum for admin_mcq_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: admin_test_data
class AdminTopicType(IntEnum):
    """Enum for admin_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class AdminStatus(IntEnum):
    """Enum for admin_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: asset_categories
class AssetCategoriesStatus(IntEnum):
    """Enum for asset_categories.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: assets
class AssetsType(IntEnum):
    """Enum for assets.type"""
    AMYPO = 1
    ACADEMIC = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "Amypo",
            2: "Academic",
        }
        return labels.get(value, "Unknown")


class AssetsStatus(IntEnum):
    """Enum for assets.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: b2c_coding_result
class B2CTopicType(IntEnum):
    """Enum for b2c_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class B2CType(IntEnum):
    """Enum for b2c_coding_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class B2CStatus(IntEnum):
    """Enum for b2c_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: b2c_mcq_result
class B2CTopicType(IntEnum):
    """Enum for b2c_mcq_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class B2CType(IntEnum):
    """Enum for b2c_mcq_result.type"""
    FILLUPS = 1
    MCQ = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "fillups",
            2: "mcq",
        }
        return labels.get(value, "Unknown")


class B2CSolveStatus(IntEnum):
    """Enum for b2c_mcq_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class B2CStatus(IntEnum):
    """Enum for b2c_mcq_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: b2c_test_data
class B2CTopicType(IntEnum):
    """Enum for b2c_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class B2CStatus(IntEnum):
    """Enum for b2c_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: batches
class BatchesStatus(IntEnum):
    """Enum for batches.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: certificates
class CertificatesType(IntEnum):
    """Enum for certificates.type"""
    COURSE = 1
    SWAYAM = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "Course",
            2: "Swayam",
        }
        return labels.get(value, "Unknown")


class CertificatesStatus(IntEnum):
    """Enum for certificates.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: ciet_2026_1_coding_result
class CietTopicType(IntEnum):
    """Enum for ciet_2026_1_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class CietType(IntEnum):
    """Enum for ciet_2026_1_coding_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class CietSolveStatus(IntEnum):
    """Enum for ciet_2026_1_coding_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class CietStatus(IntEnum):
    """Enum for ciet_2026_1_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: ciet_2026_1_test_data
class CietTopicType(IntEnum):
    """Enum for ciet_2026_1_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class CietStatus(IntEnum):
    """Enum for ciet_2026_1_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: college_department_maps
class CollegeDepartmentMapsStatus(IntEnum):
    """Enum for college_department_maps.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: college_section_maps
class CollegeSectionMapsStatus(IntEnum):
    """Enum for college_section_maps.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: colleges
class CollegesStatus(IntEnum):
    """Enum for colleges.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: compilers
class CompilersType(IntEnum):
    """Enum for compilers.type"""
    COMPILER_URL = 1
    ADP_URL = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "Compiler URL",
            2: "ADP URL",
        }
        return labels.get(value, "Unknown")


class CompilersStatus(IntEnum):
    """Enum for compilers.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: course_academic_maps
class CourseAcademicMapsType(IntEnum):
    """Enum for course_academic_maps.type"""
    PREPARE = 0
    ASSESSMENT = 1
    ASSIGNMENT = 2
    VIVA = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Prepare",
            1: "Assessment",
            2: "Assignment",
            3: "viva",
        }
        return labels.get(value, "Unknown")


class CourseAcademicMapsStatus(IntEnum):
    """Enum for course_academic_maps.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: course_prepare_timers
class CoursePrepareTimersStatus(IntEnum):
    """Enum for course_prepare_timers.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: course_staff_trainer_allocations
class CourseStaffTrainerAllocationsRole(IntEnum):
    """Enum for course_staff_trainer_allocations.role"""
    STAFF = 4
    TRAINER = 5

    @classmethod
    def get_label(cls, value):
        labels = {
            4: "Staff",
            5: "Trainer",
        }
        return labels.get(value, "Unknown")


class CourseStaffTrainerAllocationsStatus(IntEnum):
    """Enum for course_staff_trainer_allocations.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: course_topic_maps
class CourseTopicMapsStatus(IntEnum):
    """Enum for course_topic_maps.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: course_wise_segregations
class CourseWiseSegregationsCourseType(IntEnum):
    """Enum for course_wise_segregations.course_type"""
    PREPARE = 1
    ASSESSMENT = 2
    LAB = 3
    EVENT = 4
    DRIVE = 5

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "Prepare",
            2: "Assessment",
            3: "Lab",
            4: "Event",
            5: "Drive",
        }
        return labels.get(value, "Unknown")


class CourseWiseSegregationsType(IntEnum):
    """Enum for course_wise_segregations.type"""
    PREPARE = 1
    ASSESSMENT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "Prepare",
            2: "Assessment",
        }
        return labels.get(value, "Unknown")


# Enums for table: courses
class CoursesType(IntEnum):
    """Enum for courses.type"""
    PREPARE = 1
    ASSESSMENT = 2
    LAB = 3
    EVENT = 4
    DRIVE = 5

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "Prepare",
            2: "Assessment",
            3: "Lab",
            4: "Event",
            5: "Drive",
        }
        return labels.get(value, "Unknown")


class CoursesIsEdited(IntEnum):
    """Enum for courses.is_edited"""
    CLONED_COURSE_EDITED = 0
    CLONED_COURSE_NOT_EDITED = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Cloned Course edited",
            1: "Cloned Course not edited",
        }
        return labels.get(value, "Unknown")


class CoursesStatus(IntEnum):
    """Enum for courses.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: demolab_2025_2_coding_result
class DemolabTopicType(IntEnum):
    """Enum for demolab_2025_2_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class DemolabSolveStatus(IntEnum):
    """Enum for demolab_2025_2_coding_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class DemolabStatus(IntEnum):
    """Enum for demolab_2025_2_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: demolab_2025_2_test_data
class DemolabTopicType(IntEnum):
    """Enum for demolab_2025_2_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class DemolabStatus(IntEnum):
    """Enum for demolab_2025_2_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: departments
class DepartmentsStatus(IntEnum):
    """Enum for departments.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: docker_containers_map_logs
class DockerContainersMapLogsStatus(IntEnum):
    """Enum for docker_containers_map_logs.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: docker_containers_maps
class DockerContainersMapsStatus(IntEnum):
    """Enum for docker_containers_maps.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: dotlab_2025_2_coding_result
class DotlabTopicType(IntEnum):
    """Enum for dotlab_2025_2_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class DotlabType(IntEnum):
    """Enum for dotlab_2025_2_coding_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class DotlabStatus(IntEnum):
    """Enum for dotlab_2025_2_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: dotlab_2025_2_test_data
class DotlabTopicType(IntEnum):
    """Enum for dotlab_2025_2_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class DotlabStatus(IntEnum):
    """Enum for dotlab_2025_2_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: dotlab_2026_1_coding_result
class DotlabTopicType(IntEnum):
    """Enum for dotlab_2026_1_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class DotlabType(IntEnum):
    """Enum for dotlab_2026_1_coding_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class DotlabStatus(IntEnum):
    """Enum for dotlab_2026_1_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: dotlab_2026_1_mcq_result
class DotlabTopicType(IntEnum):
    """Enum for dotlab_2026_1_mcq_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class DotlabType(IntEnum):
    """Enum for dotlab_2026_1_mcq_result.type"""
    FILLUPS = 1
    MCQ = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "fillups",
            2: "mcq",
        }
        return labels.get(value, "Unknown")


class DotlabSolveStatus(IntEnum):
    """Enum for dotlab_2026_1_mcq_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class DotlabStatus(IntEnum):
    """Enum for dotlab_2026_1_mcq_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: dotlab_2026_1_test_data
class DotlabTopicType(IntEnum):
    """Enum for dotlab_2026_1_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class DotlabStatus(IntEnum):
    """Enum for dotlab_2026_1_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: institutions
class InstitutionsStatus(IntEnum):
    """Enum for institutions.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: kclas_2026_1_test_data
class KclasTopicType(IntEnum):
    """Enum for kclas_2026_1_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class KclasStatus(IntEnum):
    """Enum for kclas_2026_1_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: kits_2026_1_mcq_result
class KitsTopicType(IntEnum):
    """Enum for kits_2026_1_mcq_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class KitsType(IntEnum):
    """Enum for kits_2026_1_mcq_result.type"""
    FILLUPS = 1
    MCQ = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "fillups",
            2: "mcq",
        }
        return labels.get(value, "Unknown")


class KitsSolveStatus(IntEnum):
    """Enum for kits_2026_1_mcq_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class KitsStatus(IntEnum):
    """Enum for kits_2026_1_mcq_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: kits_2026_1_test_data
class KitsTopicType(IntEnum):
    """Enum for kits_2026_1_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class KitsStatus(IntEnum):
    """Enum for kits_2026_1_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: languages
class LanguagesStatus(IntEnum):
    """Enum for languages.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: link_coding_result
class LinkTopicType(IntEnum):
    """Enum for link_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class LinkType(IntEnum):
    """Enum for link_coding_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class LinkSolveStatus(IntEnum):
    """Enum for link_coding_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class LinkStatus(IntEnum):
    """Enum for link_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: link_test_data
class LinkStatus(IntEnum):
    """Enum for link_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: link_tests
class LinkTestsForCollegeCommon(IntEnum):
    """Enum for link_tests.for_college_common"""
    COMMON = 0
    COLLEGE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "common",
            1: "college",
        }
        return labels.get(value, "Unknown")


class LinkTestsStatus(IntEnum):
    """Enum for link_tests.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: mec_2026_1_coding_result
class MecTopicType(IntEnum):
    """Enum for mec_2026_1_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class MecType(IntEnum):
    """Enum for mec_2026_1_coding_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class MecSolveStatus(IntEnum):
    """Enum for mec_2026_1_coding_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class MecStatus(IntEnum):
    """Enum for mec_2026_1_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: mec_2026_1_test_data
class MecTopicType(IntEnum):
    """Enum for mec_2026_1_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class MecStatus(IntEnum):
    """Enum for mec_2026_1_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: niet_2026_1_coding_result
class NietTopicType(IntEnum):
    """Enum for niet_2026_1_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class NietType(IntEnum):
    """Enum for niet_2026_1_coding_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class NietSolveStatus(IntEnum):
    """Enum for niet_2026_1_coding_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class NietStatus(IntEnum):
    """Enum for niet_2026_1_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: niet_2026_1_mcq_result
class NietTopicType(IntEnum):
    """Enum for niet_2026_1_mcq_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class NietType(IntEnum):
    """Enum for niet_2026_1_mcq_result.type"""
    FILLUPS = 1
    MCQ = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "fillups",
            2: "mcq",
        }
        return labels.get(value, "Unknown")


class NietSolveStatus(IntEnum):
    """Enum for niet_2026_1_mcq_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class NietStatus(IntEnum):
    """Enum for niet_2026_1_mcq_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: niet_2026_1_test_data
class NietTopicType(IntEnum):
    """Enum for niet_2026_1_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class NietStatus(IntEnum):
    """Enum for niet_2026_1_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: pdf_banks
class PdfBanksStatus(IntEnum):
    """Enum for pdf_banks.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: portal_feedback
class PortalFeedbackStatus(IntEnum):
    """Enum for portal_feedback.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: practice_modules
class PracticeModulesDifficulty(IntEnum):
    """Enum for practice_modules.difficulty"""
    EASY = 1
    MEDUIM = 2
    HARD = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "Easy",
            2: "Meduim",
            3: "Hard",
        }
        return labels.get(value, "Unknown")


class PracticeModulesType(IntEnum):
    """Enum for practice_modules.type"""
    COURSE = 1
    TOPIC = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "Course",
            2: "Topic",
        }
        return labels.get(value, "Unknown")


class PracticeModulesModuleType(IntEnum):
    """Enum for practice_modules.module_type"""
    CODING = 1
    MCQ = 2
    FILLUPS = 3
    PROJECT = 4

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "mcq",
            3: "fillups",
            4: "project",
        }
        return labels.get(value, "Unknown")


class PracticeModulesSolveType(IntEnum):
    """Enum for practice_modules.solve_type"""
    SINGLE = 1
    BULK = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "Single",
            2: "Bulk",
        }
        return labels.get(value, "Unknown")


class PracticeModulesStatus(IntEnum):
    """Enum for practice_modules.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: practice_question_maps
class PracticeQuestionMapsType(IntEnum):
    """Enum for practice_question_maps.type"""
    CODING = 1
    MCQ = 2
    FILLUPS = 3
    PROJECT = 4

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "mcq",
            3: "fillups",
            4: "project",
        }
        return labels.get(value, "Unknown")


class PracticeQuestionMapsStatus(IntEnum):
    """Enum for practice_question_maps.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: sections
class SectionsStatus(IntEnum):
    """Enum for sections.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: skcet_2026_1_coding_result
class SkcetTopicType(IntEnum):
    """Enum for skcet_2026_1_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class SkcetType(IntEnum):
    """Enum for skcet_2026_1_coding_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class SkcetSolveStatus(IntEnum):
    """Enum for skcet_2026_1_coding_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class SkcetStatus(IntEnum):
    """Enum for skcet_2026_1_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: skcet_2026_1_mcq_result
class SkcetTopicType(IntEnum):
    """Enum for skcet_2026_1_mcq_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class SkcetType(IntEnum):
    """Enum for skcet_2026_1_mcq_result.type"""
    FILLUPS = 1
    MCQ = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "fillups",
            2: "mcq",
        }
        return labels.get(value, "Unknown")


class SkcetSolveStatus(IntEnum):
    """Enum for skcet_2026_1_mcq_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class SkcetStatus(IntEnum):
    """Enum for skcet_2026_1_mcq_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: skcet_2026_1_test_data
class SkcetTopicType(IntEnum):
    """Enum for skcet_2026_1_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class SkcetStatus(IntEnum):
    """Enum for skcet_2026_1_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: skct_2025_2_coding_result
class SkctTopicType(IntEnum):
    """Enum for skct_2025_2_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class SkctType(IntEnum):
    """Enum for skct_2025_2_coding_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class SkctSolveStatus(IntEnum):
    """Enum for skct_2025_2_coding_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class SkctStatus(IntEnum):
    """Enum for skct_2025_2_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: skct_2025_2_test_data
class SkctTopicType(IntEnum):
    """Enum for skct_2025_2_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class SkctStatus(IntEnum):
    """Enum for skct_2025_2_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: srec_2025_2_coding_result
class SrecTopicType(IntEnum):
    """Enum for srec_2025_2_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class SrecType(IntEnum):
    """Enum for srec_2025_2_coding_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class SrecSolveStatus(IntEnum):
    """Enum for srec_2025_2_coding_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class SrecStatus(IntEnum):
    """Enum for srec_2025_2_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: srec_2025_2_mcq_result
class SrecTopicType(IntEnum):
    """Enum for srec_2025_2_mcq_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class SrecType(IntEnum):
    """Enum for srec_2025_2_mcq_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class SrecSolveStatus(IntEnum):
    """Enum for srec_2025_2_mcq_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class SrecStatus(IntEnum):
    """Enum for srec_2025_2_mcq_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: srec_2025_2_test_data
class SrecTopicType(IntEnum):
    """Enum for srec_2025_2_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class SrecStatus(IntEnum):
    """Enum for srec_2025_2_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: srec_2026_1_coding_result
class SrecTopicType(IntEnum):
    """Enum for srec_2026_1_coding_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class SrecType(IntEnum):
    """Enum for srec_2026_1_coding_result.type"""
    CODING = 1
    PROJECT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "Project",
        }
        return labels.get(value, "Unknown")


class SrecSolveStatus(IntEnum):
    """Enum for srec_2026_1_coding_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class SrecStatus(IntEnum):
    """Enum for srec_2026_1_coding_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: srec_2026_1_mcq_result
class SrecTopicType(IntEnum):
    """Enum for srec_2026_1_mcq_result.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class SrecType(IntEnum):
    """Enum for srec_2026_1_mcq_result.type"""
    FILLUPS = 1
    MCQ = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "fillups",
            2: "mcq",
        }
        return labels.get(value, "Unknown")


class SrecSolveStatus(IntEnum):
    """Enum for srec_2026_1_mcq_result.solve_status"""
    UNSOLVED = 0
    PARTIAL = 1
    SOLVED = 2
    SAVED = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "unsolved",
            1: "partial",
            2: "Solved",
            3: "saved",
        }
        return labels.get(value, "Unknown")


class SrecStatus(IntEnum):
    """Enum for srec_2026_1_mcq_result.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: srec_2026_1_test_data
class SrecTopicType(IntEnum):
    """Enum for srec_2026_1_test_data.topic_type"""
    PRACTICE = 0
    ASSESSMENT = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "practice",
            1: "assessment",
        }
        return labels.get(value, "Unknown")


class SrecStatus(IntEnum):
    """Enum for srec_2026_1_test_data.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: staff_trainer_feedback
class StaffTrainerFeedbackStatus(IntEnum):
    """Enum for staff_trainer_feedback.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: standard_qb_codings
class StandardQbCodingsApprovalStatus(IntEnum):
    """Enum for standard_qb_codings.approval_status"""
    APPROVED = 1
    REJECTED = 2
    PENDING = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "approved",
            2: "rejected",
            3: "pending",
        }
        return labels.get(value, "Unknown")


class StandardQbCodingsStatus(IntEnum):
    """Enum for standard_qb_codings.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: standard_qb_courses
class StandardQbCoursesStatus(IntEnum):
    """Enum for standard_qb_courses.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: standard_qb_mcqs
class StandardQbMcqsQuestionCategory(IntEnum):
    """Enum for standard_qb_mcqs.question_category"""
    FILLUPS = 1
    MCQ = 2
    VERBALS = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "fillups",
            2: "mcq",
            3: "verbals",
        }
        return labels.get(value, "Unknown")


class StandardQbMcqsQuestionType(IntEnum):
    """Enum for standard_qb_mcqs.question_type"""
    SINGLE_OPTION = 1
    MULTI_OPTIONS = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "single option",
            2: "multi options",
        }
        return labels.get(value, "Unknown")


# Enums for table: standard_qb_projects
class StandardQbProjectsQuestionType(IntEnum):
    """Enum for standard_qb_projects.question_type"""
    ONLY_QUESTION = 1
    PROJECT_QUESTION = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "only question",
            2: "project question",
        }
        return labels.get(value, "Unknown")


class StandardQbProjectsStatus(IntEnum):
    """Enum for standard_qb_projects.status"""
    DELETED = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "deleted",
            1: "active",
        }
        return labels.get(value, "Unknown")


# Enums for table: standard_qb_topics
class StandardQbTopicsStatus(IntEnum):
    """Enum for standard_qb_topics.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: tags
class TagsType(IntEnum):
    """Enum for tags.type"""
    NORMAL_TAG = 1
    COMPANY_TAG = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "normal tag",
            2: "company tag",
        }
        return labels.get(value, "Unknown")


class TagsStatus(IntEnum):
    """Enum for tags.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: test_modules
class TestModulesModuletype(IntEnum):
    """Enum for test_modules.moduleType"""
    CODING = 1
    MCQ = 2
    FILLUPS = 3
    PROJECT = 4

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "mcq",
            3: "fillups",
            4: "project",
        }
        return labels.get(value, "Unknown")


class TestModulesUniquequestion(IntEnum):
    """Enum for test_modules.uniqueQuestion"""
    COMMON = 0
    UNIQUE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "common",
            1: "unique",
        }
        return labels.get(value, "Unknown")


class TestModulesStatus(IntEnum):
    """Enum for test_modules.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: test_question_maps
class TestQuestionMapsType(IntEnum):
    """Enum for test_question_maps.type"""
    CODING = 1
    MCQ = 2
    FILLUPS = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "coding",
            2: "mcq",
            3: "fillups",
        }
        return labels.get(value, "Unknown")


class TestQuestionMapsStatus(IntEnum):
    """Enum for test_question_maps.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: tests
class TestsStatus(IntEnum):
    """Enum for tests.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: titles
class TitlesStatus(IntEnum):
    """Enum for titles.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: topics
class TopicsCategory(IntEnum):
    """Enum for topics.category"""
    PREPARE = 1
    ASSIGNMENT = 2

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "Prepare",
            2: "Assignment",
        }
        return labels.get(value, "Unknown")


class TopicsStatus(IntEnum):
    """Enum for topics.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: users
class UsersStatus(IntEnum):
    """Enum for users.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "inactive",
            1: "active",
        }
        return labels.get(value, "Unknown")


class UsersRole(IntEnum):
    """Enum for users.role"""
    SUPER_ADMIN = 1
    ADMIN = 2
    COLLEGE_ADMIN = 3
    STAFF = 4
    TRAINER = 5
    CONTENT = 6
    STUDENT = 7

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "super admin",
            2: "admin",
            3: "college admin",
            4: "staff",
            5: "Trainer",
            6: "content",
            7: "student",
        }
        return labels.get(value, "Unknown")


class UsersGender(IntEnum):
    """Enum for users.gender"""
    MALE = 1
    FEMALE = 2
    OTHER = 3

    @classmethod
    def get_label(cls, value):
        labels = {
            1: "male",
            2: "female",
            3: "other",
        }
        return labels.get(value, "Unknown")


# Enums for table: viva_question_bank
class VivaQuestionBankStatus(IntEnum):
    """Enum for viva_question_bank.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")


# Enums for table: viva_result
class VivaResultStatus(IntEnum):
    """Enum for viva_result.status"""
    INACTIVE = 0
    ACTIVE = 1

    @classmethod
    def get_label(cls, value):
        labels = {
            0: "Inactive",
            1: "Active",
        }
        return labels.get(value, "Unknown")

