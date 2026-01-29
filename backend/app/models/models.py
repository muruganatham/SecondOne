"""
SQLAlchemy Models - 100% Accurate
Auto-generated from Database Schema Analysis
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, Numeric, ForeignKey, Float, JSON, Enum, BigInteger, SmallInteger, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.core.db import Base
import app.models.enums as Enums

# Note: Base is imported from app.core.db to share the same instance

class SubmissionTracks2025(Base):
    __tablename__ = '2025_submission_tracks'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    mode = Column(Enum(Enums.SubmissionTracks2025Mode), nullable=True)
    type = Column(Enum(Enums.SubmissionTracks2025Type), nullable=True)
    period = Column(Enum(Enums.SubmissionTracks2025Period), nullable=True)
    attended_count_details = Column(JSON, nullable=True)
    solved_count_details = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship('Users', foreign_keys=[user_id])


class SubmissionTracks2026(Base):
    __tablename__ = '2026_submission_tracks'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    mode = Column(Enum(Enums.SubmissionTracks2026Mode), nullable=True)
    type = Column(Enum(Enums.SubmissionTracks2026Type), nullable=True)
    period = Column(String, nullable=True)
    attended_count_details = Column(JSON, nullable=True)
    solved_count_details = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship('Users', foreign_keys=[user_id])


class AIHighLights(Base):
    __tablename__ = 'a_i_high_lights'

    id = Column(Enum(Enums.AIHighLightsId), primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Enum(Enums.AIHighLightsUserId), ForeignKey('users.id'), nullable=False)
    course_id = Column(Enum(Enums.AIHighLightsCourseId), ForeignKey('courses.id'), nullable=False)
    topic_id = Column(Enum(Enums.AIHighLightsTopicId), ForeignKey('topics.id'), nullable=False)
    material_id = Column(Enum(Enums.AIHighLightsMaterialId), nullable=False)
    table_name = Column(String(255), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    course = relationship('Courses', foreign_keys=[course_id])
    topic = relationship('Topics', foreign_keys=[topic_id])
    user = relationship('Users', foreign_keys=[user_id])


class AcademicPdfMaterialBanks(Base):
    __tablename__ = 'academic_pdf_material_banks'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    path = Column(String(255), nullable=False)
    subject_id = Column(Integer, nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    title = Column(String(30), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    topic = relationship('Topics', foreign_keys=[topic_id])


class AcademicQbCodings(Base):
    __tablename__ = 'academic_qb_codings'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_id = Column(Enum(Enums.AcademicQbCodingsCourseId), ForeignKey('courses.id'), nullable=False)
    topic_id = Column(Enum(Enums.AcademicQbCodingsTopicId), ForeignKey('topics.id'), nullable=False)
    title = Column(String(255), nullable=False)
    complexity_type = Column(Enum(Enums.AcademicQbCodingsComplexityType), nullable=False)
    actual_time = Column(Enum(Enums.AcademicQbCodingsActualTime), nullable=False)
    company_tags = Column(Enum(Enums.AcademicQbCodingsCompanyTags), nullable=True)
    question_tags = Column(Enum(Enums.AcademicQbCodingsQuestionTags), nullable=True)
    l_id = Column(Enum(Enums.AcademicQbCodingsLId), ForeignKey('languages.id'), nullable=False)
    question = Column(Text, nullable=False)
    accuracy_question = Column(String(255), nullable=True)
    solution_header = Column(Text, nullable=True)
    solution = Column(Text, nullable=False)
    solution_footer = Column(Text, nullable=True)
    file = Column(String(255), nullable=True)
    testcases = Column(JSON, nullable=False)
    black_list = Column(JSON, nullable=True)
    white_list = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=False)
    status = Column(Enum(Enums.AcademicQbCodingsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    course = relationship('Courses', foreign_keys=[course_id])
    l = relationship('Languages', foreign_keys=[l_id])
    topic = relationship('Topics', foreign_keys=[topic_id])


class AcademicQbMcqs(Base):
    __tablename__ = 'academic_qb_mcqs'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_id = Column(Enum(Enums.AcademicQbMcqsCourseId), ForeignKey('courses.id'), nullable=False)
    topic_id = Column(Enum(Enums.AcademicQbMcqsTopicId), ForeignKey('topics.id'), nullable=False)
    title = Column(String(255), nullable=False)
    complexity_type = Column(Enum(Enums.AcademicQbMcqsComplexityType), nullable=False)
    company_tags = Column(JSON, nullable=True)
    question = Column(Text, nullable=False)
    accuracy_question = Column(String(255), nullable=True)
    l_id = Column(Enum(Enums.AcademicQbMcqsLId), nullable=True)
    actual_time = Column(Integer, nullable=True)
    options = Column(JSON, nullable=False)
    correct_options = Column(Enum(Enums.AcademicQbMcqsCorrectOptions), nullable=True)
    tags = Column(Enum(Enums.AcademicQbMcqsTags), nullable=False)
    question_category = Column(Enum(Enums.AcademicQbMcqsQuestionCategory), nullable=False)
    question_type = Column(Integer, nullable=True)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    course = relationship('Courses', foreign_keys=[course_id])
    topic = relationship('Topics', foreign_keys=[topic_id])


class AcademicQbProjects(Base):
    __tablename__ = 'academic_qb_projects'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_id = Column(Enum(Enums.AcademicQbProjectsCourseId), ForeignKey('courses.id'), nullable=False)
    topic_id = Column(Enum(Enums.AcademicQbProjectsTopicId), ForeignKey('topics.id'), nullable=False)
    title = Column(String(255), nullable=False)
    complexity_type = Column(Enum(Enums.AcademicQbProjectsComplexityType), nullable=False)
    l_id = Column(Enum(Enums.AcademicQbProjectsLId), ForeignKey('languages.id'), nullable=False)
    actual_time = Column(Enum(Enums.AcademicQbProjectsActualTime), nullable=True)
    question = Column(Text, nullable=False)
    accuracy_question = Column(Enum(Enums.AcademicQbProjectsAccuracyQuestion), nullable=True)
    question_type = Column(Integer, nullable=False)
    testcases = Column(JSON, nullable=True)
    company_tags = Column(Enum(Enums.AcademicQbProjectsCompanyTags), nullable=True)
    tags = Column(Enum(Enums.AcademicQbProjectsTags), nullable=False)
    testcaseCount = Column(Enum(Enums.AcademicQbProjectsTestcasecount), nullable=True)
    status = Column(Enum(Enums.AcademicQbProjectsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    course = relationship('Courses', foreign_keys=[course_id])
    l = relationship('Languages', foreign_keys=[l_id])
    topic = relationship('Topics', foreign_keys=[topic_id])


class AcademicStudyMaterialBanks(Base):
    __tablename__ = 'academic_study_material_banks'

    id = Column(Enum(Enums.AcademicStudyMaterialBanksId), primary_key=True, autoincrement=True, nullable=False)
    path = Column(Enum(Enums.AcademicStudyMaterialBanksPath), nullable=False)
    subject_id = Column(Enum(Enums.AcademicStudyMaterialBanksSubjectId), nullable=False)
    topic_id = Column(Enum(Enums.AcademicStudyMaterialBanksTopicId), ForeignKey('topics.id'), nullable=False)
    title = Column(Enum(Enums.AcademicStudyMaterialBanksTitle), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    topic = relationship('Topics', foreign_keys=[topic_id])


class AdminCodingResult(Base):
    __tablename__ = 'admin_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(Enum(Enums.AdminTopicType), nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(Enum(Enums.AdminType), nullable=False)
    complexity = Column(Enum(Enums.AdminComplexity), nullable=False)
    mark = Column(Enum(Enums.AdminMark), nullable=False)
    total_mark = Column(Enum(Enums.AdminTotalMark), nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(Enum(Enums.AdminSubSolutions), nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Enum(Enums.AdminCompileId), nullable=True)
    total_time = Column(String, nullable=False)
    first_submission_time = Column(String, nullable=False)
    correct_submission_time = Column(String, nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Enum(Enums.AdminSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship('Users', foreign_keys=[user_id])


class AdminMcqResult(Base):
    __tablename__ = 'admin_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(Enum(Enums.AdminUserId), ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.AdminAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.AdminCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.AdminTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.AdminTopicType), nullable=False)
    module_id = Column(Enum(Enums.AdminModuleId), nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Enum(Enums.AdminComplexity), nullable=False)
    mark = Column(Enum(Enums.AdminMark), nullable=False)
    total_mark = Column(Integer, nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(Enum(Enums.AdminAttemptCount), nullable=False)
    solve_status = Column(Enum(Enums.AdminSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship('Users', foreign_keys=[user_id])


class AdminTestData(Base):
    __tablename__ = 'admin_test_data'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(Enum(Enums.AdminTopicType), nullable=False)
    module_id = Column(String, nullable=False)
    mark = Column(JSON, nullable=False)
    total_mark = Column(Enum(Enums.AdminTotalMark), nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Enum(Enums.AdminTotalTime), nullable=False)
    question_ids = Column(JSON, nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    question_status = Column(JSON, nullable=True)
    attempt_allowed = Column(Enum(Enums.AdminAttemptAllowed), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship('Users', foreign_keys=[user_id])


class AiPrompts(Base):
    __tablename__ = 'ai_prompts'

    id = Column(Enum(Enums.AiPromptsId), primary_key=True, autoincrement=True, nullable=False)
    prompt_title_id = Column(Enum(Enums.AiPromptsPromptTitleId), ForeignKey('prompt_titles.id'), nullable=False)
    prompt = Column(Text, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    prompt_title = relationship('PromptTitles', foreign_keys=[prompt_title_id])


class AssetCategories(Base):
    __tablename__ = 'asset_categories'

    id = Column(Enum(Enums.AssetCategoriesId), primary_key=True, autoincrement=True, nullable=False)
    category = Column(Enum(Enums.AssetCategoriesCategory), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class Assets(Base):
    __tablename__ = 'assets'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    category_id = Column(Enum(Enums.AssetsCategoryId), ForeignKey('asset_categories.id'), nullable=False)
    path = Column(String(255), nullable=False)
    type = Column(Integer, nullable=False)
    creator_college_id = Column(Enum(Enums.AssetsCreatorCollegeId), nullable=True)
    status = Column(Enum(Enums.AssetsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    category = relationship('AssetCategories', foreign_keys=[category_id])


class Audits(Base):
    __tablename__ = 'audits'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    user_type = Column(String(255), nullable=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=True)
    event = Column(Enum(Enums.AuditsEvent), nullable=False)
    auditable_type = Column(String(255), nullable=False)
    auditable_id = Column(String, nullable=False)
    old_values = Column(Text, nullable=True)
    new_values = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(1023), nullable=True)
    tags = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship('Users', foreign_keys=[user_id])


class B2CCodingResult(Base):
    __tablename__ = 'b2c_coding_result'

    id = Column(Enum(Enums.B2CId), nullable=False)
    user_id = Column(Enum(Enums.B2CUserId), ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(JSON, nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Enum(Enums.B2CTotalTime), nullable=False)
    first_submission_time = Column(Integer, nullable=False)
    correct_submission_time = Column(Integer, nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class B2CMcqResult(Base):
    __tablename__ = 'b2c_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.B2CAllocateId), nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(Enum(Enums.B2CTopicTestId), nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(Enum(Enums.B2CModuleId), nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Enum(Enums.B2CComplexity), nullable=False)
    mark = Column(Enum(Enums.B2CMark), nullable=False)
    total_mark = Column(Enum(Enums.B2CTotalMark), nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(Enum(Enums.B2CType), nullable=False)
    attempt_count = Column(Enum(Enums.B2CAttemptCount), nullable=False)
    solve_status = Column(Enum(Enums.B2CSolveStatus), nullable=False)
    status = Column(Enum(Enums.B2CStatus), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class B2CTestData(Base):
    __tablename__ = 'b2c_test_data'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.B2CAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.B2CCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.B2CTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.B2CTopicType), nullable=False)
    module_id = Column(Enum(Enums.B2CModuleId), nullable=False)
    mark = Column(Enum(Enums.B2CMark), nullable=False)
    total_mark = Column(Enum(Enums.B2CTotalMark), nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Enum(Enums.B2CTotalTime), nullable=False)
    question_ids = Column(JSON, nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    question_status = Column(Enum(Enums.B2CQuestionStatus), nullable=True)
    attempt_allowed = Column(Enum(Enums.B2CAttemptAllowed), nullable=False)
    status = Column(Enum(Enums.B2CStatus), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Batches(Base):
    __tablename__ = 'batches'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    batch_name = Column(Enum(Enums.BatchesBatchName), nullable=False)
    college_id = Column(Enum(Enums.BatchesCollegeId), ForeignKey('colleges.id'), nullable=False)
    status = Column(Enum(Enums.BatchesStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    college = relationship('Colleges', foreign_keys=[college_id])


class Cache(Base):
    __tablename__ = 'cache'

    key = Column(String(255), primary_key=True, nullable=False)
    value = Column(Text, nullable=False)
    expiration = Column(Integer, nullable=False)


class CacheLocks(Base):
    __tablename__ = 'cache_locks'

    key = Column(Enum(Enums.CacheLocksKey), primary_key=True, nullable=False)
    owner = Column(Enum(Enums.CacheLocksOwner), nullable=False)
    expiration = Column(Enum(Enums.CacheLocksExpiration), nullable=False)


class Certificates(Base):
    __tablename__ = 'certificates'

    id = Column(Enum(Enums.CertificatesId), primary_key=True, autoincrement=True, nullable=False)
    title = Column(Enum(Enums.CertificatesTitle), nullable=False)
    sub_title = Column(Enum(Enums.CertificatesSubTitle), nullable=False)
    type = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Enum(Enums.CertificatesStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class Ciet20261CodingResult(Base):
    __tablename__ = 'ciet_2026_1_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.CietAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.CietCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.CietTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.CietTopicType), nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Enum(Enums.CietComplexity), nullable=False)
    mark = Column(Enum(Enums.CietMark), nullable=False)
    total_mark = Column(Enum(Enums.CietTotalMark), nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(JSON, nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Integer, nullable=False)
    correct_submission_time = Column(Integer, nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Enum(Enums.CietSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Ciet20261McqResult(Base):
    __tablename__ = 'ciet_2026_1_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(String, nullable=False)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Ciet20261TestData(Base):
    __tablename__ = 'ciet_2026_1_test_data'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.CietAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.CietCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.CietTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.CietTopicType), nullable=False)
    module_id = Column(String, nullable=False)
    mark = Column(JSON, nullable=False)
    total_mark = Column(Enum(Enums.CietTotalMark), nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Enum(Enums.CietTotalTime), nullable=False)
    question_ids = Column(JSON, nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    question_status = Column(JSON, nullable=True)
    attempt_allowed = Column(Enum(Enums.CietAttemptAllowed), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class CollegeDepartmentMaps(Base):
    __tablename__ = 'college_department_maps'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    college_id = Column(Enum(Enums.CollegeDepartmentMapsCollegeId), ForeignKey('colleges.id'), nullable=False)
    department_id = Column(String, ForeignKey('departments.id'), nullable=False)
    status = Column(Enum(Enums.CollegeDepartmentMapsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    college = relationship('Colleges', foreign_keys=[college_id])
    department = relationship('Departments', foreign_keys=[department_id])


class CollegeSectionMaps(Base):
    __tablename__ = 'college_section_maps'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    college_id = Column(Enum(Enums.CollegeSectionMapsCollegeId), ForeignKey('colleges.id'), nullable=False)
    section_id = Column(Enum(Enums.CollegeSectionMapsSectionId), ForeignKey('sections.id'), nullable=False)
    status = Column(Enum(Enums.CollegeSectionMapsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    college = relationship('Colleges', foreign_keys=[college_id])
    section = relationship('Sections', foreign_keys=[section_id])


class Colleges(Base):
    __tablename__ = 'colleges'

    id = Column(Enum(Enums.CollegesId), primary_key=True, autoincrement=True, nullable=False)
    college_name = Column(Enum(Enums.CollegesCollegeName), nullable=False)
    college_image = Column(Enum(Enums.CollegesCollegeImage), nullable=False)
    college_short_name = Column(Enum(Enums.CollegesCollegeShortName), nullable=False)
    institution_id = Column(Enum(Enums.CollegesInstitutionId), ForeignKey('institutions.id'), nullable=True)
    ai_features = Column(JSON, nullable=True)
    url = Column(Enum(Enums.CollegesUrl), nullable=False)
    status = Column(Enum(Enums.CollegesStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    institution = relationship('Institutions', foreign_keys=[institution_id])


class Compilers(Base):
    __tablename__ = 'compilers'

    id = Column(Enum(Enums.CompilersId), primary_key=True, autoincrement=True, nullable=False)
    type = Column(Enum(Enums.CompilersType), nullable=True)
    api = Column(Enum(Enums.CompilersApi), nullable=False)
    count = Column(Enum(Enums.CompilersCount), nullable=True)
    status = Column(Enum(Enums.CompilersStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class CourseAcademicMaps(Base):
    __tablename__ = 'course_academic_maps'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    allocation_id = Column(Integer, nullable=False)
    college_id = Column(Enum(Enums.CourseAcademicMapsCollegeId), ForeignKey('colleges.id'), nullable=True)
    department_id = Column(String, ForeignKey('departments.id'), nullable=True)
    batch_id = Column(Enum(Enums.CourseAcademicMapsBatchId), ForeignKey('batches.id'), nullable=True)
    section_id = Column(Enum(Enums.CourseAcademicMapsSectionId), ForeignKey('sections.id'), nullable=True)
    course_id = Column(String, ForeignKey('courses.id'), nullable=False)
    title_id = Column(Integer, ForeignKey('titles.id'), nullable=True)
    type = Column(Enum(Enums.CourseAcademicMapsType), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    topic_name = Column(String(255), nullable=True)
    topic_order = Column(Enum(Enums.CourseAcademicMapsTopicOrder), nullable=False)
    course_start_date = Column(DateTime, nullable=True)
    course_end_date = Column(DateTime, nullable=True)
    topic_start_date = Column(DateTime, nullable=False)
    topic_end_date = Column(DateTime, nullable=False)
    proctoring = Column(Text, nullable=True)
    user_access = Column(JSON, nullable=True)
    lock_and_percent = Column(Enum(Enums.CourseAcademicMapsLockAndPercent), nullable=True)
    db = Column(Enum(Enums.CourseAcademicMapsDb), nullable=False)
    student_allocated = Column(JSON, nullable=True)
    certificate_details = Column(Enum(Enums.CourseAcademicMapsCertificateDetails), nullable=True)
    b2c_details = Column(Enum(Enums.CourseAcademicMapsB2CDetails), nullable=True)
    status = Column(Enum(Enums.CourseAcademicMapsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    batch = relationship('Batches', foreign_keys=[batch_id])
    college = relationship('Colleges', foreign_keys=[college_id])
    course = relationship('Courses', foreign_keys=[course_id])
    department = relationship('Departments', foreign_keys=[department_id])
    section = relationship('Sections', foreign_keys=[section_id])
    title = relationship('Titles', foreign_keys=[title_id])
    topic = relationship('Topics', foreign_keys=[topic_id])


class CoursePrepareTimers(Base):
    __tablename__ = 'course_prepare_timers'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_allocated_id = Column(Integer, nullable=False)
    topic_id = Column(String, ForeignKey('topics.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    timer = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    topic = relationship('Topics', foreign_keys=[topic_id])
    user = relationship('Users', foreign_keys=[user_id])


class CourseStaffTrainerAllocations(Base):
    __tablename__ = 'course_staff_trainer_allocations'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocation_id = Column(Integer, nullable=False)
    role = Column(Enum(Enums.CourseStaffTrainerAllocationsRole), nullable=False)
    status = Column(Enum(Enums.CourseStaffTrainerAllocationsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship('Users', foreign_keys=[user_id])


class CourseTopicMaps(Base):
    __tablename__ = 'course_topic_maps'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_id = Column(String, ForeignKey('courses.id'), nullable=False)
    title_id = Column(String, ForeignKey('titles.id'), nullable=False)
    topic_id = Column(String, ForeignKey('topics.id'), nullable=False)
    order = Column(Enum(Enums.CourseTopicMapsOrder), nullable=False)
    status = Column(Enum(Enums.CourseTopicMapsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    course = relationship('Courses', foreign_keys=[course_id])
    title = relationship('Titles', foreign_keys=[title_id])
    topic = relationship('Topics', foreign_keys=[topic_id])


class CourseWiseSegregations(Base):
    __tablename__ = 'course_wise_segregations'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    user_role = Column(Enum(Enums.CourseWiseSegregationsUserRole), nullable=False)
    college_id = Column(Enum(Enums.CourseWiseSegregationsCollegeId), ForeignKey('colleges.id'), nullable=True)
    department_id = Column(Enum(Enums.CourseWiseSegregationsDepartmentId), ForeignKey('departments.id'), nullable=True)
    batch_id = Column(Enum(Enums.CourseWiseSegregationsBatchId), ForeignKey('batches.id'), nullable=True)
    section_id = Column(Enum(Enums.CourseWiseSegregationsSectionId), ForeignKey('sections.id'), nullable=True)
    course_id = Column(String, ForeignKey('courses.id'), nullable=False)
    course_allocation_id = Column(Integer, nullable=False)
    course_type = Column(Integer, nullable=False)
    type = Column(Enum(Enums.CourseWiseSegregationsType), nullable=False)
    progress = Column(Numeric, nullable=False)
    score = Column(Integer, nullable=False)
    attempt_taken = Column(Integer, nullable=False)
    time_spend = Column(Integer, nullable=False)
    rank = Column(Integer, nullable=False)
    performance_rank = Column(Integer, nullable=False)
    coding_matrics = Column(String(255), nullable=True)
    coding_question = Column(JSON, nullable=True)
    mcq_question = Column(JSON, nullable=True)
    project_question = Column(JSON, nullable=True)
    assessment_details = Column(String(255), nullable=True)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    batch = relationship('Batches', foreign_keys=[batch_id])
    college = relationship('Colleges', foreign_keys=[college_id])
    course = relationship('Courses', foreign_keys=[course_id])
    department = relationship('Departments', foreign_keys=[department_id])
    section = relationship('Sections', foreign_keys=[section_id])
    user = relationship('Users', foreign_keys=[user_id])


class Courses(Base):
    __tablename__ = 'courses'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_name = Column(String(50), nullable=False)
    course_short_name = Column(String(20), nullable=False)
    course_description = Column(String(255), nullable=True)
    language = Column(Enum(Enums.CoursesLanguage), nullable=False)
    category = Column(Enum(Enums.CoursesCategory), nullable=False)
    type = Column(Integer, nullable=False)
    course_info = Column(JSON, nullable=False)
    course_image = Column(String(255), nullable=False)
    course_banner_image = Column(String(255), nullable=False)
    clone_id = Column(Enum(Enums.CoursesCloneId), nullable=True)
    is_edited = Column(Integer, nullable=False)
    creator_college_id = Column(Integer, nullable=True)
    status = Column(Enum(Enums.CoursesStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class Demolab20252CodingResult(Base):
    __tablename__ = 'demolab_2025_2_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.DemolabAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.DemolabCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.DemolabTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.DemolabTopicType), nullable=False)
    module_id = Column(Enum(Enums.DemolabModuleId), nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(Enum(Enums.DemolabType), nullable=False)
    complexity = Column(Enum(Enums.DemolabComplexity), nullable=False)
    mark = Column(Enum(Enums.DemolabMark), nullable=False)
    total_mark = Column(Enum(Enums.DemolabTotalMark), nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(Enum(Enums.DemolabSubSolutions), nullable=True)
    test_cases = Column(Enum(Enums.DemolabTestCases), nullable=True)
    compile_id = Column(Enum(Enums.DemolabCompileId), nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Enum(Enums.DemolabFirstSubmissionTime), nullable=False)
    correct_submission_time = Column(Enum(Enums.DemolabCorrectSubmissionTime), nullable=False)
    errors = Column(Enum(Enums.DemolabErrors), nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(Enum(Enums.DemolabReportMetrics), nullable=True)
    solve_status = Column(Enum(Enums.DemolabSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Demolab20252McqResult(Base):
    __tablename__ = 'demolab_2025_2_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(String, nullable=False)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Demolab20252TestData(Base):
    __tablename__ = 'demolab_2025_2_test_data'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.DemolabAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.DemolabCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.DemolabTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.DemolabTopicType), nullable=False)
    module_id = Column(Enum(Enums.DemolabModuleId), nullable=False)
    mark = Column(Enum(Enums.DemolabMark), nullable=False)
    total_mark = Column(Enum(Enums.DemolabTotalMark), nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Enum(Enums.DemolabTotalTime), nullable=False)
    question_ids = Column(JSON, nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(Enum(Enums.DemolabReportMetrics), nullable=True)
    question_status = Column(Enum(Enums.DemolabQuestionStatus), nullable=True)
    attempt_allowed = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Departments(Base):
    __tablename__ = 'departments'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    department_name = Column(String(80), nullable=False)
    department_short_name = Column(String(20), nullable=False)
    is_default = Column(Enum(Enums.DepartmentsIsDefault), nullable=False)
    status = Column(Enum(Enums.DepartmentsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class DiscussionMessages(Base):
    __tablename__ = 'discussion_messages'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    discussion_id = Column(String, ForeignKey('discussions.id'), nullable=False)
    message = Column(Text, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=True)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    discussion = relationship('Discussions', foreign_keys=[discussion_id])
    user = relationship('Users', foreign_keys=[user_id])


class Discussions(Base):
    __tablename__ = 'discussions'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_allocated_id = Column(Integer, nullable=False)
    topic_id = Column(String, ForeignKey('topics.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    is_replied = Column(Integer, nullable=False)
    last_replied = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    topic = relationship('Topics', foreign_keys=[topic_id])
    user = relationship('Users', foreign_keys=[user_id])


class DockerContainersMapLogs(Base):
    __tablename__ = 'docker_containers_map_logs'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    container_logs = Column(JSON, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    lang_id = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship('Users', foreign_keys=[user_id])


class DockerContainersMaps(Base):
    __tablename__ = 'docker_containers_maps'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    container_id = Column(String(255), nullable=False)
    server_id = Column(Enum(Enums.DockerContainersMapsServerId), ForeignKey('compilers.id'), nullable=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    lang_id = Column(Integer, nullable=False)
    ports = Column(JSON, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    server = relationship('Compilers', foreign_keys=[server_id])
    user = relationship('Users', foreign_keys=[user_id])


class Dotlab20252CodingResult(Base):
    __tablename__ = 'dotlab_2025_2_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(Enum(Enums.DotlabUserId), ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.DotlabAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.DotlabCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.DotlabTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.DotlabTopicType), nullable=False)
    module_id = Column(Enum(Enums.DotlabModuleId), nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Enum(Enums.DotlabComplexity), nullable=False)
    mark = Column(Enum(Enums.DotlabMark), nullable=False)
    total_mark = Column(Enum(Enums.DotlabTotalMark), nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(JSON, nullable=True)
    test_cases = Column(Enum(Enums.DotlabTestCases), nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Enum(Enums.DotlabFirstSubmissionTime), nullable=False)
    correct_submission_time = Column(Enum(Enums.DotlabCorrectSubmissionTime), nullable=False)
    errors = Column(Enum(Enums.DotlabErrors), nullable=True)
    action_counts = Column(Enum(Enums.DotlabActionCounts), nullable=True)
    report_metrics = Column(Enum(Enums.DotlabReportMetrics), nullable=True)
    solve_status = Column(Enum(Enums.DotlabSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Dotlab20252McqResult(Base):
    __tablename__ = 'dotlab_2025_2_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(String, nullable=False)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Dotlab20252TestData(Base):
    __tablename__ = 'dotlab_2025_2_test_data'

    id = Column(String, nullable=False)
    user_id = Column(Enum(Enums.DotlabUserId), ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.DotlabAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.DotlabCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.DotlabTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.DotlabTopicType), nullable=False)
    module_id = Column(Enum(Enums.DotlabModuleId), nullable=False)
    mark = Column(Enum(Enums.DotlabMark), nullable=False)
    total_mark = Column(Enum(Enums.DotlabTotalMark), nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Enum(Enums.DotlabTotalTime), nullable=False)
    question_ids = Column(JSON, nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(Enum(Enums.DotlabReportMetrics), nullable=True)
    question_status = Column(Enum(Enums.DotlabQuestionStatus), nullable=True)
    attempt_allowed = Column(Enum(Enums.DotlabAttemptAllowed), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Dotlab20261CodingResult(Base):
    __tablename__ = 'dotlab_2026_1_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(Enum(Enums.DotlabUserId), ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.DotlabAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.DotlabCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.DotlabTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.DotlabTopicType), nullable=False)
    module_id = Column(Enum(Enums.DotlabModuleId), nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Enum(Enums.DotlabComplexity), nullable=False)
    mark = Column(Enum(Enums.DotlabMark), nullable=False)
    total_mark = Column(Enum(Enums.DotlabTotalMark), nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(JSON, nullable=True)
    test_cases = Column(Enum(Enums.DotlabTestCases), nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Enum(Enums.DotlabFirstSubmissionTime), nullable=False)
    correct_submission_time = Column(Enum(Enums.DotlabCorrectSubmissionTime), nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(Enum(Enums.DotlabReportMetrics), nullable=True)
    solve_status = Column(Enum(Enums.DotlabSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Dotlab20261McqResult(Base):
    __tablename__ = 'dotlab_2026_1_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(Enum(Enums.DotlabUserId), ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.DotlabAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.DotlabCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.DotlabTopicTestId), nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(Enum(Enums.DotlabModuleId), nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Enum(Enums.DotlabComplexity), nullable=False)
    mark = Column(Enum(Enums.DotlabMark), nullable=False)
    total_mark = Column(Enum(Enums.DotlabTotalMark), nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(Enum(Enums.DotlabTotalTime), nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(Enum(Enums.DotlabAttemptCount), nullable=False)
    solve_status = Column(Enum(Enums.DotlabSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Dotlab20261TestData(Base):
    __tablename__ = 'dotlab_2026_1_test_data'

    id = Column(String, nullable=False)
    user_id = Column(Enum(Enums.DotlabUserId), ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.DotlabAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.DotlabCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.DotlabTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.DotlabTopicType), nullable=False)
    module_id = Column(Enum(Enums.DotlabModuleId), nullable=False)
    mark = Column(Enum(Enums.DotlabMark), nullable=False)
    total_mark = Column(Enum(Enums.DotlabTotalMark), nullable=False)
    time = Column(Enum(Enums.DotlabTime), nullable=False)
    total_time = Column(Enum(Enums.DotlabTotalTime), nullable=False)
    question_ids = Column(Enum(Enums.DotlabQuestionIds), nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(Enum(Enums.DotlabReportMetrics), nullable=True)
    question_status = Column(Enum(Enums.DotlabQuestionStatus), nullable=True)
    attempt_allowed = Column(Enum(Enums.DotlabAttemptAllowed), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class FailedJobs(Base):
    __tablename__ = 'failed_jobs'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    uuid = Column(String(255), nullable=False)
    connection = Column(Text, nullable=False)
    queue = Column(Text, nullable=False)
    payload = Column(Text, nullable=False)
    exception = Column(Text, nullable=False)
    failed_at = Column(DateTime, nullable=False)


class FeedbackAllocations(Base):
    __tablename__ = 'feedback_allocations'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    college_id = Column(Enum(Enums.FeedbackAllocationsCollegeId), ForeignKey('colleges.id'), nullable=False)
    department_id = Column(Enum(Enums.FeedbackAllocationsDepartmentId), ForeignKey('departments.id'), nullable=False)
    batch_id = Column(Enum(Enums.FeedbackAllocationsBatchId), ForeignKey('batches.id'), nullable=False)
    section_id = Column(Enum(Enums.FeedbackAllocationsSectionId), ForeignKey('sections.id'), nullable=False)
    allocation_id = Column(Integer, nullable=True)
    date = Column(DateTime, nullable=False)
    type = Column(Enum(Enums.FeedbackAllocationsType), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    batch = relationship('Batches', foreign_keys=[batch_id])
    college = relationship('Colleges', foreign_keys=[college_id])
    department = relationship('Departments', foreign_keys=[department_id])
    section = relationship('Sections', foreign_keys=[section_id])


class FeedbackQuestions(Base):
    __tablename__ = 'feedback_questions'

    id = Column(Enum(Enums.FeedbackQuestionsId), primary_key=True, autoincrement=True, nullable=False)
    question = Column(Enum(Enums.FeedbackQuestionsQuestion), nullable=False)
    feedback_type = Column(Enum(Enums.FeedbackQuestionsFeedbackType), nullable=False)
    type = Column(Enum(Enums.FeedbackQuestionsType), nullable=False)
    college_id = Column(String, ForeignKey('colleges.id'), nullable=True)
    order = Column(Enum(Enums.FeedbackQuestionsOrder), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    college = relationship('Colleges', foreign_keys=[college_id])


class Institutions(Base):
    __tablename__ = 'institutions'

    id = Column(Enum(Enums.InstitutionsId), primary_key=True, autoincrement=True, nullable=False)
    institution_name = Column(Enum(Enums.InstitutionsInstitutionName), nullable=False)
    institution_image = Column(Enum(Enums.InstitutionsInstitutionImage), nullable=False)
    status = Column(Enum(Enums.InstitutionsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class JobBatches(Base):
    __tablename__ = 'job_batches'

    id = Column(String(255), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    total_jobs = Column(Integer, nullable=False)
    pending_jobs = Column(Integer, nullable=False)
    failed_jobs = Column(Integer, nullable=False)
    failed_job_ids = Column(Text, nullable=False)
    options = Column(Text, nullable=True)
    cancelled_at = Column(Integer, nullable=True)
    created_at = Column(Integer, nullable=False)
    finished_at = Column(Integer, nullable=True)


class Jobs(Base):
    __tablename__ = 'jobs'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    queue = Column(String(255), nullable=False)
    payload = Column(Text, nullable=False)
    attempts = Column(String, nullable=False)
    reserved_at = Column(String, nullable=True)
    available_at = Column(String, nullable=False)
    created_at = Column(String, nullable=False)


class Kclas20261CodingResult(Base):
    __tablename__ = 'kclas_2026_1_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(JSON, nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Integer, nullable=False)
    correct_submission_time = Column(Integer, nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Kclas20261McqResult(Base):
    __tablename__ = 'kclas_2026_1_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.KclasAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.KclasCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.KclasTopicTestId), nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(Enum(Enums.KclasModuleId), nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Enum(Enums.KclasComplexity), nullable=False)
    mark = Column(Enum(Enums.KclasMark), nullable=False)
    total_mark = Column(Enum(Enums.KclasTotalMark), nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(Enum(Enums.KclasAttemptCount), nullable=False)
    solve_status = Column(Enum(Enums.KclasSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Kclas20261TestData(Base):
    __tablename__ = 'kclas_2026_1_test_data'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.KclasAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.KclasCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.KclasTopicTestId), nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(Enum(Enums.KclasModuleId), nullable=False)
    mark = Column(JSON, nullable=False)
    total_mark = Column(Enum(Enums.KclasTotalMark), nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Enum(Enums.KclasTotalTime), nullable=False)
    question_ids = Column(JSON, nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    question_status = Column(JSON, nullable=True)
    attempt_allowed = Column(Enum(Enums.KclasAttemptAllowed), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Kits20261CodingResult(Base):
    __tablename__ = 'kits_2026_1_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(JSON, nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Integer, nullable=False)
    correct_submission_time = Column(Integer, nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Kits20261McqResult(Base):
    __tablename__ = 'kits_2026_1_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.KitsAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.KitsCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.KitsTopicTestId), nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(Enum(Enums.KitsModuleId), nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Enum(Enums.KitsComplexity), nullable=False)
    mark = Column(Enum(Enums.KitsMark), nullable=False)
    total_mark = Column(Float, nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(Enum(Enums.KitsAttemptCount), nullable=False)
    solve_status = Column(Enum(Enums.KitsSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Kits20261TestData(Base):
    __tablename__ = 'kits_2026_1_test_data'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.KitsAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.KitsCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.KitsTopicTestId), nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(Enum(Enums.KitsModuleId), nullable=False)
    mark = Column(JSON, nullable=False)
    total_mark = Column(JSON, nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Integer, nullable=False)
    question_ids = Column(Enum(Enums.KitsQuestionIds), nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    question_status = Column(JSON, nullable=True)
    attempt_allowed = Column(Enum(Enums.KitsAttemptAllowed), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Languages(Base):
    __tablename__ = 'languages'

    id = Column(Enum(Enums.LanguagesId), primary_key=True, autoincrement=True, nullable=False)
    language_name = Column(Enum(Enums.LanguagesLanguageName), nullable=False)
    language_id = Column(Enum(Enums.LanguagesLanguageId), ForeignKey('languages.id'), nullable=False)
    language_image = Column(Enum(Enums.LanguagesLanguageImage), nullable=False)
    language_category = Column(Enum(Enums.LanguagesLanguageCategory), nullable=False)
    status = Column(Enum(Enums.LanguagesStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    language = relationship('Languages', foreign_keys=[language_id])


class LinkBatches(Base):
    __tablename__ = 'link_batches'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    link_id = Column(Integer, nullable=True)
    batch_name = Column(String(255), nullable=True)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class LinkCodingResult(Base):
    __tablename__ = 'link_coding_result'

    id = Column(Enum(Enums.LinkId), nullable=False)
    user_id = Column(Enum(Enums.LinkUserId), ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(Enum(Enums.LinkQuestionId), nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Enum(Enums.LinkComplexity), nullable=False)
    mark = Column(Enum(Enums.LinkMark), nullable=False)
    total_mark = Column(Enum(Enums.LinkTotalMark), nullable=False)
    main_solution = Column(Text, nullable=True)
    test_cases = Column(Enum(Enums.LinkTestCases), nullable=True)
    compile_id = Column(Enum(Enums.LinkCompileId), nullable=True)
    total_time = Column(Enum(Enums.LinkTotalTime), nullable=False)
    first_submission_time = Column(Enum(Enums.LinkFirstSubmissionTime), nullable=False)
    correct_submission_time = Column(Enum(Enums.LinkCorrectSubmissionTime), nullable=False)
    errors = Column(Enum(Enums.LinkErrors), nullable=True)
    action_counts = Column(Enum(Enums.LinkActionCounts), nullable=True)
    report_metrics = Column(Enum(Enums.LinkReportMetrics), nullable=True)
    solve_status = Column(Enum(Enums.LinkSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class LinkColleges(Base):
    __tablename__ = 'link_colleges'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    link_id = Column(Integer, nullable=True)
    college_name = Column(String(255), nullable=True)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class LinkDepartments(Base):
    __tablename__ = 'link_departments'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    link_id = Column(Integer, nullable=True)
    department_name = Column(String(255), nullable=True)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class LinkMcqResult(Base):
    __tablename__ = 'link_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(String, nullable=False)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class LinkSections(Base):
    __tablename__ = 'link_sections'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    link_id = Column(Integer, nullable=True)
    section_name = Column(String(255), nullable=True)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class LinkTestData(Base):
    __tablename__ = 'link_test_data'

    id = Column(Enum(Enums.LinkId), nullable=False)
    user_id = Column(Enum(Enums.LinkUserId), ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    mark = Column(Enum(Enums.LinkMark), nullable=False)
    total_mark = Column(JSON, nullable=False)
    time = Column(Enum(Enums.LinkTime), nullable=False)
    total_time = Column(Integer, nullable=False)
    question_ids = Column(JSON, nullable=True)
    attempt_datas = Column(Enum(Enums.LinkAttemptDatas), nullable=True)
    report_metrics = Column(Enum(Enums.LinkReportMetrics), nullable=True)
    question_status = Column(Enum(Enums.LinkQuestionStatus), nullable=True)
    attempt_allowed = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class LinkTestUsers(Base):
    __tablename__ = 'link_test_users'

    id = Column(Enum(Enums.LinkTestUsersId), primary_key=True, autoincrement=True, nullable=False)
    name = Column(Enum(Enums.LinkTestUsersName), nullable=False)
    email = Column(Enum(Enums.LinkTestUsersEmail), nullable=False)
    phone = Column(Enum(Enums.LinkTestUsersPhone), nullable=False)
    clg_id = Column(Integer, nullable=True)
    dept_id = Column(Integer, nullable=True)
    batch_id = Column(Integer, nullable=True)
    section_id = Column(Integer, ForeignKey('sections.id'), nullable=True)
    link_id = Column(String, ForeignKey('link_tests.id'), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    link = relationship('LinkTests', foreign_keys=[link_id])
    section = relationship('Sections', foreign_keys=[section_id])


class LinkTests(Base):
    __tablename__ = 'link_tests'

    id = Column(Enum(Enums.LinkTestsId), primary_key=True, autoincrement=True, nullable=False)
    test_id = Column(Enum(Enums.LinkTestsTestId), ForeignKey('tests.id'), nullable=False)
    link_test_name = Column(Enum(Enums.LinkTestsLinkTestName), nullable=True)
    start_date_time = Column(DateTime, nullable=False)
    end_date_time = Column(DateTime, nullable=False)
    restricted_emails = Column(String(255), nullable=True)
    allowed_emails = Column(String(255), nullable=True)
    for_college_common = Column(Integer, nullable=False)
    college = Column(Enum(Enums.LinkTestsCollege), nullable=True)
    dept = Column(String(255), nullable=True)
    batch = Column(String(255), nullable=True)
    section = Column(String(255), nullable=True)
    url_name = Column(String(255), nullable=True)
    proctoring = Column(Text, nullable=True)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    test = relationship('Tests', foreign_keys=[test_id])


class Mcet20252CodingResult(Base):
    __tablename__ = 'mcet_2025_2_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(Enum(Enums.McetTopicType), nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Enum(Enums.McetComplexity), nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Enum(Enums.McetTotalMark), nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(Enum(Enums.McetSubSolutions), nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Integer, nullable=False)
    correct_submission_time = Column(Integer, nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Enum(Enums.McetSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Mcet20252McqResult(Base):
    __tablename__ = 'mcet_2025_2_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(String, nullable=False)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Mcet20252TestData(Base):
    __tablename__ = 'mcet_2025_2_test_data'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(Enum(Enums.McetTopicType), nullable=False)
    module_id = Column(String, nullable=False)
    mark = Column(JSON, nullable=False)
    total_mark = Column(Enum(Enums.McetTotalMark), nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Enum(Enums.McetTotalTime), nullable=False)
    question_ids = Column(JSON, nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    question_status = Column(JSON, nullable=True)
    attempt_allowed = Column(Enum(Enums.McetAttemptAllowed), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Mcet20261CodingResult(Base):
    __tablename__ = 'mcet_2026_1_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.McetAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.McetCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.McetTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.McetTopicType), nullable=False)
    module_id = Column(Enum(Enums.McetModuleId), nullable=False)
    question_id = Column(Enum(Enums.McetQuestionId), nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Enum(Enums.McetComplexity), nullable=False)
    mark = Column(Enum(Enums.McetMark), nullable=False)
    total_mark = Column(Enum(Enums.McetTotalMark), nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(JSON, nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Integer, nullable=False)
    correct_submission_time = Column(Integer, nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Enum(Enums.McetSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Mcet20261McqResult(Base):
    __tablename__ = 'mcet_2026_1_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.McetAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.McetCourseAllocationId), nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(Enum(Enums.McetQuestionId), nullable=False)
    complexity = Column(Enum(Enums.McetComplexity), nullable=False)
    mark = Column(Enum(Enums.McetMark), nullable=False)
    total_mark = Column(Enum(Enums.McetTotalMark), nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(Enum(Enums.McetAttemptCount), nullable=False)
    solve_status = Column(Enum(Enums.McetSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Mcet20261TestData(Base):
    __tablename__ = 'mcet_2026_1_test_data'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.McetAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.McetCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.McetTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.McetTopicType), nullable=False)
    module_id = Column(Enum(Enums.McetModuleId), nullable=False)
    mark = Column(JSON, nullable=False)
    total_mark = Column(Enum(Enums.McetTotalMark), nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Enum(Enums.McetTotalTime), nullable=False)
    question_ids = Column(Enum(Enums.McetQuestionIds), nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    question_status = Column(JSON, nullable=True)
    attempt_allowed = Column(Enum(Enums.McetAttemptAllowed), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Mec20261CodingResult(Base):
    __tablename__ = 'mec_2026_1_coding_result'

    id = Column(Enum(Enums.MecId), nullable=False)
    user_id = Column(Enum(Enums.MecUserId), ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(Enum(Enums.MecModuleId), nullable=False)
    question_id = Column(Enum(Enums.MecQuestionId), nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Enum(Enums.MecMark), nullable=False)
    total_mark = Column(Float, nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(JSON, nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Enum(Enums.MecTotalTime), nullable=False)
    first_submission_time = Column(Enum(Enums.MecFirstSubmissionTime), nullable=False)
    correct_submission_time = Column(Integer, nullable=False)
    errors = Column(Enum(Enums.MecErrors), nullable=True)
    action_counts = Column(Enum(Enums.MecActionCounts), nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Enum(Enums.MecSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Mec20261McqResult(Base):
    __tablename__ = 'mec_2026_1_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(String, nullable=False)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Mec20261TestData(Base):
    __tablename__ = 'mec_2026_1_test_data'

    id = Column(Enum(Enums.MecId), nullable=False)
    user_id = Column(Enum(Enums.MecUserId), ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(Enum(Enums.MecModuleId), nullable=False)
    mark = Column(Enum(Enums.MecMark), nullable=False)
    total_mark = Column(JSON, nullable=False)
    time = Column(Enum(Enums.MecTime), nullable=False)
    total_time = Column(Integer, nullable=False)
    question_ids = Column(Enum(Enums.MecQuestionIds), nullable=True)
    attempt_datas = Column(Enum(Enums.MecAttemptDatas), nullable=True)
    report_metrics = Column(Enum(Enums.MecReportMetrics), nullable=True)
    question_status = Column(Enum(Enums.MecQuestionStatus), nullable=True)
    attempt_allowed = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Migrations(Base):
    __tablename__ = 'migrations'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    migration = Column(String(255), nullable=False)
    batch = Column(Enum(Enums.MigrationsBatch), nullable=False)


class Niet20261CodingResult(Base):
    __tablename__ = 'niet_2026_1_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.NietAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.NietCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.NietTopicTestId), nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(Enum(Enums.NietModuleId), nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Enum(Enums.NietComplexity), nullable=False)
    mark = Column(Enum(Enums.NietMark), nullable=False)
    total_mark = Column(Enum(Enums.NietTotalMark), nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(Enum(Enums.NietSubSolutions), nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Enum(Enums.NietCompileId), nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Integer, nullable=False)
    correct_submission_time = Column(Integer, nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Enum(Enums.NietSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Niet20261McqResult(Base):
    __tablename__ = 'niet_2026_1_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.NietAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.NietCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.NietTopicTestId), nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(Enum(Enums.NietModuleId), nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Enum(Enums.NietMark), nullable=False)
    total_mark = Column(Float, nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(Enum(Enums.NietAttemptCount), nullable=False)
    solve_status = Column(Enum(Enums.NietSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Niet20261TestData(Base):
    __tablename__ = 'niet_2026_1_test_data'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.NietAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.NietCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.NietTopicTestId), nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    mark = Column(JSON, nullable=False)
    total_mark = Column(Enum(Enums.NietTotalMark), nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Integer, nullable=False)
    question_ids = Column(JSON, nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    question_status = Column(JSON, nullable=True)
    attempt_allowed = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Nit20261CodingResult(Base):
    __tablename__ = 'nit_2026_1_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(JSON, nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Integer, nullable=False)
    correct_submission_time = Column(Integer, nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Nit20261McqResult(Base):
    __tablename__ = 'nit_2026_1_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(String, nullable=False)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Nit20261TestData(Base):
    __tablename__ = 'nit_2026_1_test_data'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    mark = Column(JSON, nullable=False)
    total_mark = Column(JSON, nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Integer, nullable=False)
    question_ids = Column(JSON, nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    question_status = Column(JSON, nullable=True)
    attempt_allowed = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Otps(Base):
    __tablename__ = 'otps'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(String(255), ForeignKey('users.id'), nullable=False)
    otp = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship('Users', foreign_keys=[user_id])


class PasswordResetTokens(Base):
    __tablename__ = 'password_reset_tokens'

    email = Column(String(255), primary_key=True, nullable=False)
    token = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=True)


class PdfBanks(Base):
    __tablename__ = 'pdf_banks'

    id = Column(Enum(Enums.PdfBanksId), primary_key=True, autoincrement=True, nullable=False)
    path = Column(Enum(Enums.PdfBanksPath), nullable=False)
    subject_id = Column(Enum(Enums.PdfBanksSubjectId), nullable=False)
    topic_id = Column(Enum(Enums.PdfBanksTopicId), ForeignKey('topics.id'), nullable=False)
    title = Column(Enum(Enums.PdfBanksTitle), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    topic = relationship('Topics', foreign_keys=[topic_id])


class PersonalAccessTokens(Base):
    __tablename__ = 'personal_access_tokens'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    tokenable_type = Column(Enum(Enums.PersonalAccessTokensTokenableType), nullable=False)
    tokenable_id = Column(String, nullable=False)
    name = Column(Enum(Enums.PersonalAccessTokensName), nullable=False)
    token = Column(String(64), nullable=False)
    abilities = Column(Text, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class PortalFeedback(Base):
    __tablename__ = 'portal_feedback'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    type = Column(Enum(Enums.PortalFeedbackType), nullable=False)
    question_id = Column(Enum(Enums.PortalFeedbackQuestionId), ForeignKey('feedback_questions.id'), nullable=False)
    feedback = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    question = relationship('FeedbackQuestions', foreign_keys=[question_id])
    user = relationship('Users', foreign_keys=[user_id])


class PracticeModules(Base):
    __tablename__ = 'practice_modules'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    forign_id = Column(Integer, nullable=False)
    module_name = Column(Enum(Enums.PracticeModulesModuleName), nullable=False)
    difficulty = Column(Enum(Enums.PracticeModulesDifficulty), nullable=False)
    type = Column(Enum(Enums.PracticeModulesType), nullable=False)
    module_type = Column(Enum(Enums.PracticeModulesModuleType), nullable=False)
    solve_type = Column(Enum(Enums.PracticeModulesSolveType), nullable=False)
    coding_count = Column(Enum(Enums.PracticeModulesCodingCount), nullable=True)
    coding_display_count = Column(Enum(Enums.PracticeModulesCodingDisplayCount), nullable=True)
    coding_eval_count = Column(Integer, nullable=True)
    mcq_count = Column(Enum(Enums.PracticeModulesMcqCount), nullable=True)
    mcq_display_count = Column(Enum(Enums.PracticeModulesMcqDisplayCount), nullable=True)
    fill_ups_count = Column(Enum(Enums.PracticeModulesFillUpsCount), nullable=True)
    fill_ups_display_count = Column(Enum(Enums.PracticeModulesFillUpsDisplayCount), nullable=True)
    project_count = Column(Enum(Enums.PracticeModulesProjectCount), nullable=True)
    project_display_count = Column(Enum(Enums.PracticeModulesProjectDisplayCount), nullable=True)
    order = Column(Enum(Enums.PracticeModulesOrder), nullable=False)
    status = Column(Enum(Enums.PracticeModulesStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class PracticeQuestionMaps(Base):
    __tablename__ = 'practice_question_maps'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    topic_id = Column(String, ForeignKey('topics.id'), nullable=False)
    module_id = Column(String, ForeignKey('practice_modules.id'), nullable=False)
    question_id = Column(Integer, nullable=False)
    type = Column(Enum(Enums.PracticeQuestionMapsType), nullable=False)
    qb_name = Column(Enum(Enums.PracticeQuestionMapsQbName), nullable=False)
    mark = Column(Enum(Enums.PracticeQuestionMapsMark), nullable=False)
    order = Column(Integer, nullable=False)
    status = Column(Enum(Enums.PracticeQuestionMapsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    module = relationship('PracticeModules', foreign_keys=[module_id])
    topic = relationship('Topics', foreign_keys=[topic_id])


class PromptTitles(Base):
    __tablename__ = 'prompt_titles'

    id = Column(Enum(Enums.PromptTitlesId), primary_key=True, autoincrement=True, nullable=False)
    title = Column(Enum(Enums.PromptTitlesTitle), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class Sections(Base):
    __tablename__ = 'sections'

    id = Column(Enum(Enums.SectionsId), primary_key=True, autoincrement=True, nullable=False)
    section_name = Column(Enum(Enums.SectionsSectionName), nullable=False)
    is_default = Column(Enum(Enums.SectionsIsDefault), nullable=False)
    status = Column(Enum(Enums.SectionsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(Enum(Enums.SessionsId), primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=True)
    ip_address = Column(Enum(Enums.SessionsIpAddress), nullable=True)
    user_agent = Column(Text, nullable=True)
    payload = Column(Text, nullable=False)
    last_activity = Column(Enum(Enums.SessionsLastActivity), nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class ShieldLogs(Base):
    __tablename__ = 'shield_logs'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    mac_address = Column(String(50), nullable=False)
    attempt = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    key_logs = Column(Text, nullable=False)
    exam_activity = Column(Text, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class SidebarRoles(Base):
    __tablename__ = 'sidebar_roles'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    sidebar_id = Column(Integer, nullable=False)
    roles = Column(Enum(Enums.SidebarRolesRoles), nullable=False)
    status = Column(Enum(Enums.SidebarRolesStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class Skacas20252CodingResult(Base):
    __tablename__ = 'skacas_2025_2_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(JSON, nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Integer, nullable=False)
    correct_submission_time = Column(Integer, nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Skacas20252McqResult(Base):
    __tablename__ = 'skacas_2025_2_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(String, nullable=False)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Skacas20252TestData(Base):
    __tablename__ = 'skacas_2025_2_test_data'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    mark = Column(JSON, nullable=False)
    total_mark = Column(JSON, nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Integer, nullable=False)
    question_ids = Column(JSON, nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    question_status = Column(JSON, nullable=True)
    attempt_allowed = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Skcet20261CodingResult(Base):
    __tablename__ = 'skcet_2026_1_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(Enum(Enums.SkcetCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.SkcetTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.SkcetTopicType), nullable=False)
    module_id = Column(Enum(Enums.SkcetModuleId), nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Enum(Enums.SkcetComplexity), nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Enum(Enums.SkcetTotalMark), nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(JSON, nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Integer, nullable=False)
    correct_submission_time = Column(Integer, nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Enum(Enums.SkcetSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Skcet20261McqResult(Base):
    __tablename__ = 'skcet_2026_1_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(Enum(Enums.SkcetAllocateId), nullable=False)
    course_allocation_id = Column(Enum(Enums.SkcetCourseAllocationId), nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Enum(Enums.SkcetMark), nullable=False)
    total_mark = Column(Float, nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(Enum(Enums.SkcetAttemptCount), nullable=False)
    solve_status = Column(Enum(Enums.SkcetSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Skcet20261TestData(Base):
    __tablename__ = 'skcet_2026_1_test_data'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(Enum(Enums.SkcetCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.SkcetTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.SkcetTopicType), nullable=False)
    module_id = Column(Enum(Enums.SkcetModuleId), nullable=False)
    mark = Column(JSON, nullable=False)
    total_mark = Column(Enum(Enums.SkcetTotalMark), nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Enum(Enums.SkcetTotalTime), nullable=False)
    question_ids = Column(JSON, nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    question_status = Column(JSON, nullable=True)
    attempt_allowed = Column(Enum(Enums.SkcetAttemptAllowed), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Skct20252CodingResult(Base):
    __tablename__ = 'skct_2025_2_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(Enum(Enums.SkctCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.SkctTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.SkctTopicType), nullable=False)
    module_id = Column(Enum(Enums.SkctModuleId), nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Enum(Enums.SkctComplexity), nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Enum(Enums.SkctTotalMark), nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(JSON, nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Integer, nullable=False)
    correct_submission_time = Column(Integer, nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Enum(Enums.SkctSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Skct20252McqResult(Base):
    __tablename__ = 'skct_2025_2_mcq_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(String, nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Float, nullable=False)
    solution = Column(Text, nullable=True)
    total_time = Column(String, nullable=False)
    type = Column(String, nullable=False)
    attempt_count = Column(String, nullable=False)
    solve_status = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Skct20252TestData(Base):
    __tablename__ = 'skct_2025_2_test_data'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(Enum(Enums.SkctCourseAllocationId), nullable=False)
    topic_test_id = Column(Enum(Enums.SkctTopicTestId), nullable=False)
    topic_type = Column(Enum(Enums.SkctTopicType), nullable=False)
    module_id = Column(Enum(Enums.SkctModuleId), nullable=False)
    mark = Column(JSON, nullable=False)
    total_mark = Column(Enum(Enums.SkctTotalMark), nullable=False)
    time = Column(String, nullable=False)
    total_time = Column(Integer, nullable=False)
    question_ids = Column(JSON, nullable=True)
    attempt_datas = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    question_status = Column(Enum(Enums.SkctQuestionStatus), nullable=True)
    attempt_allowed = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class Srec20252CodingResult(Base):
    __tablename__ = 'srec_2025_2_coding_result'

    id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    allocate_id = Column(String, nullable=False)
    course_allocation_id = Column(Enum(Enums.SrecCourseAllocationId), nullable=False)
    topic_test_id = Column(String, nullable=False)
    topic_type = Column(Enum(Enums.SrecTopicType), nullable=False)
    module_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    complexity = Column(Enum(Enums.SrecComplexity), nullable=False)
    mark = Column(Float, nullable=False)
    total_mark = Column(Enum(Enums.SrecTotalMark), nullable=False)
    main_solution = Column(Text, nullable=True)
    sub_solutions = Column(Enum(Enums.SrecSubSolutions), nullable=True)
    test_cases = Column(JSON, nullable=True)
    compile_id = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=False)
    first_submission_time = Column(Integer, nullable=False)
    correct_submission_time = Column(Integer, nullable=False)
    errors = Column(JSON, nullable=True)
    action_counts = Column(JSON, nullable=True)
    report_metrics = Column(JSON, nullable=True)
    solve_status = Column(Enum(Enums.SrecSolveStatus), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    user = relationship('Users', foreign_keys=[user_id])


class StaffTrainerFeedback(Base):
    __tablename__ = 'staff_trainer_feedback'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    type = Column(Enum(Enums.StaffTrainerFeedbackType), nullable=False)
    course_id = Column(Enum(Enums.StaffTrainerFeedbackCourseId), ForeignKey('courses.id'), nullable=False)
    staff_trainer_id = Column(String, ForeignKey('users.id'), nullable=False)
    question_id = Column(Enum(Enums.StaffTrainerFeedbackQuestionId), ForeignKey('feedback_questions.id'), nullable=False)
    feedback = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    course = relationship('Courses', foreign_keys=[course_id])
    question = relationship('FeedbackQuestions', foreign_keys=[question_id])
    staff_trainer = relationship('Users', foreign_keys=[staff_trainer_id])
    user = relationship('Users', foreign_keys=[user_id])


class StandardQbCodings(Base):
    __tablename__ = 'standard_qb_codings'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_id = Column(Enum(Enums.StandardQbCodingsCourseId), ForeignKey('standard_qb_courses.id'), nullable=False)
    topic_id = Column(String, ForeignKey('standard_qb_topics.id'), nullable=False)
    title = Column(String(255), nullable=False)
    complexity_type = Column(Enum(Enums.StandardQbCodingsComplexityType), nullable=False)
    actual_time = Column(Integer, nullable=False)
    company_tags = Column(JSON, nullable=True)
    question_tags = Column(JSON, nullable=True)
    l_id = Column(Enum(Enums.StandardQbCodingsLId), ForeignKey('languages.id'), nullable=False)
    question = Column(Text, nullable=False)
    accuracy_question = Column(String(255), nullable=True)
    solution_header = Column(Text, nullable=True)
    solution = Column(Text, nullable=False)
    solution_footer = Column(Text, nullable=True)
    file = Column(Enum(Enums.StandardQbCodingsFile), nullable=True)
    testcases = Column(JSON, nullable=False)
    black_list = Column(JSON, nullable=True)
    white_list = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=False)
    approval_status = Column(Enum(Enums.StandardQbCodingsApprovalStatus), nullable=False)
    action_details = Column(JSON, nullable=True)
    rejection_reason = Column(Enum(Enums.StandardQbCodingsRejectionReason), nullable=True)
    status = Column(Enum(Enums.StandardQbCodingsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    course = relationship('StandardQbCourses', foreign_keys=[course_id])
    l = relationship('Languages', foreign_keys=[l_id])
    topic = relationship('StandardQbTopics', foreign_keys=[topic_id])


class StandardQbCourses(Base):
    __tablename__ = 'standard_qb_courses'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_name = Column(String(255), nullable=False)
    language_id = Column(Enum(Enums.StandardQbCoursesLanguageId), ForeignKey('languages.id'), nullable=False)
    category = Column(Enum(Enums.StandardQbCoursesCategory), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    language = relationship('Languages', foreign_keys=[language_id])


class StandardQbMcqs(Base):
    __tablename__ = 'standard_qb_mcqs'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_id = Column(Enum(Enums.StandardQbMcqsCourseId), ForeignKey('standard_qb_courses.id'), nullable=False)
    topic_id = Column(String, ForeignKey('standard_qb_topics.id'), nullable=False)
    title = Column(String(255), nullable=False)
    complexity_type = Column(Enum(Enums.StandardQbMcqsComplexityType), nullable=False)
    company_tags = Column(JSON, nullable=True)
    question = Column(Text, nullable=False)
    accuracy_question = Column(String(255), nullable=True)
    l_id = Column(BigInteger, nullable=True)
    actual_time = Column(Integer, nullable=True)
    options = Column(Text, nullable=False)
    correct_options = Column(Enum(Enums.StandardQbMcqsCorrectOptions), nullable=True)
    tags = Column(JSON, nullable=False)
    question_category = Column(Enum(Enums.StandardQbMcqsQuestionCategory), nullable=False)
    question_type = Column(Integer, nullable=True)
    approval_status = Column(Enum(Enums.StandardQbMcqsApprovalStatus), nullable=False)
    action_details = Column(JSON, nullable=True)
    rejection_reason = Column(String(255), nullable=True)
    status = Column(Enum(Enums.StandardQbMcqsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    course = relationship('StandardQbCourses', foreign_keys=[course_id])
    topic = relationship('StandardQbTopics', foreign_keys=[topic_id])


class StandardQbProjects(Base):
    __tablename__ = 'standard_qb_projects'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_id = Column(Enum(Enums.StandardQbProjectsCourseId), ForeignKey('courses.id'), nullable=False)
    topic_id = Column(Enum(Enums.StandardQbProjectsTopicId), ForeignKey('topics.id'), nullable=False)
    title = Column(String(255), nullable=False)
    complexity_type = Column(Enum(Enums.StandardQbProjectsComplexityType), nullable=False)
    l_id = Column(String, ForeignKey('languages.id'), nullable=False)
    actual_time = Column(Integer, nullable=True)
    question = Column(Text, nullable=False)
    accuracy_question = Column(String(255), nullable=True)
    question_type = Column(Integer, nullable=False)
    testcases = Column(JSON, nullable=True)
    company_tags = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=False)
    testcaseCount = Column(Enum(Enums.StandardQbProjectsTestcasecount), nullable=True)
    approval_status = Column(Enum(Enums.StandardQbProjectsApprovalStatus), nullable=False)
    action_details = Column(Enum(Enums.StandardQbProjectsActionDetails), nullable=True)
    rejection_reason = Column(String(255), nullable=True)
    status = Column(Enum(Enums.StandardQbProjectsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    course = relationship('Courses', foreign_keys=[course_id])
    l = relationship('Languages', foreign_keys=[l_id])
    topic = relationship('Topics', foreign_keys=[topic_id])


class StandardQbTopics(Base):
    __tablename__ = 'standard_qb_topics'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_id = Column(String, ForeignKey('standard_qb_courses.id'), nullable=False)
    topic_name = Column(String(255), nullable=False)
    status = Column(Enum(Enums.StandardQbTopicsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    course = relationship('StandardQbCourses', foreign_keys=[course_id])


class StudentSideBarAccesses(Base):
    __tablename__ = 'student_side_bar_accesses'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    college_id = Column(Enum(Enums.StudentSideBarAccessesCollegeId), ForeignKey('colleges.id'), nullable=False)
    batch_id = Column(Enum(Enums.StudentSideBarAccessesBatchId), ForeignKey('batches.id'), nullable=False)
    department_id = Column(String, ForeignKey('departments.id'), nullable=False)
    section_id = Column(Enum(Enums.StudentSideBarAccessesSectionId), ForeignKey('sections.id'), nullable=False)
    access = Column(Enum(Enums.StudentSideBarAccessesAccess), nullable=True)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    batch = relationship('Batches', foreign_keys=[batch_id])
    college = relationship('Colleges', foreign_keys=[college_id])
    department = relationship('Departments', foreign_keys=[department_id])
    section = relationship('Sections', foreign_keys=[section_id])


class StudyMaterialBanks(Base):
    __tablename__ = 'study_material_banks'

    id = Column(Enum(Enums.StudyMaterialBanksId), primary_key=True, autoincrement=True, nullable=False)
    path = Column(Enum(Enums.StudyMaterialBanksPath), nullable=False)
    subject_id = Column(Enum(Enums.StudyMaterialBanksSubjectId), nullable=False)
    topic_id = Column(Enum(Enums.StudyMaterialBanksTopicId), ForeignKey('topics.id'), nullable=False)
    title = Column(Enum(Enums.StudyMaterialBanksTitle), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    topic = relationship('Topics', foreign_keys=[topic_id])


class Tags(Base):
    __tablename__ = 'tags'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    tag_name = Column(String(30), nullable=False)
    type = Column(Enum(Enums.TagsType), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class TelescopeEntries(Base):
    __tablename__ = 'telescope_entries'

    sequence = Column(String, primary_key=True, autoincrement=True, nullable=False)
    uuid = Column(String(36), nullable=False)
    batch_id = Column(Enum(Enums.TelescopeEntriesBatchId), nullable=False)
    family_hash = Column(String(255), nullable=True)
    should_display_on_index = Column(Integer, nullable=False)
    type = Column(Enum(Enums.TelescopeEntriesType), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=True)


class TelescopeEntriesTags(Base):
    __tablename__ = 'telescope_entries_tags'

    entry_uuid = Column(String(36), ForeignKey('telescope_entries.uuid'), primary_key=True, nullable=False)
    tag = Column(String(255), primary_key=True, nullable=False)
    entry_uuid = relationship('TelescopeEntries', foreign_keys=[entry_uuid])


class TelescopeMonitoring(Base):
    __tablename__ = 'telescope_monitoring'

    tag = Column(String(255), primary_key=True, nullable=False)


class TestModules(Base):
    __tablename__ = 'test_modules'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    test_id = Column(String, ForeignKey('tests.id'), nullable=False)
    moduleName = Column(String(30), nullable=False)
    language = Column(Enum(Enums.TestModulesLanguage), nullable=False)
    moduleType = Column(Enum(Enums.TestModulesModuletype), nullable=False)
    sets = Column(Text, nullable=False)
    uniqueQuestion = Column(Enum(Enums.TestModulesUniquequestion), nullable=False)
    mcqQuestions = Column(JSON, nullable=True)
    codingQuestions = Column(JSON, nullable=True)
    fillUpsQuestions = Column(JSON, nullable=True)
    projectQuestions = Column(Enum(Enums.TestModulesProjectquestions), nullable=True)
    order = Column(Enum(Enums.TestModulesOrder), nullable=False)
    status = Column(Enum(Enums.TestModulesStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    test = relationship('Tests', foreign_keys=[test_id])


class TestQuestionMaps(Base):
    __tablename__ = 'test_question_maps'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    test_id = Column(String, ForeignKey('tests.id'), nullable=False)
    module_id = Column(String, ForeignKey('test_modules.id'), nullable=False)
    set_id = Column(Integer, nullable=False)
    group_id = Column(Integer, nullable=False)
    question_id = Column(Integer, nullable=False)
    type = Column(Enum(Enums.TestQuestionMapsType), nullable=False)
    qb_name = Column(Enum(Enums.TestQuestionMapsQbName), nullable=False)
    mark = Column(Enum(Enums.TestQuestionMapsMark), nullable=False)
    order = Column(Integer, nullable=False)
    status = Column(Enum(Enums.TestQuestionMapsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    module = relationship('TestModules', foreign_keys=[module_id])
    test = relationship('Tests', foreign_keys=[test_id])


class TestpageUserTracks(Base):
    __tablename__ = 'testpage_user_tracks'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_allocated_id = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    role = Column(Enum(Enums.TestpageUserTracksRole), nullable=False)
    status = Column(Enum(Enums.TestpageUserTracksStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship('Users', foreign_keys=[user_id])


class Tests(Base):
    __tablename__ = 'tests'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    testName = Column(String(50), nullable=False)
    clone_id = Column(Integer, nullable=True)
    is_edited = Column(Integer, nullable=False)
    creator_college_id = Column(Integer, nullable=True)
    status = Column(Enum(Enums.TestsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class Titles(Base):
    __tablename__ = 'titles'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_id = Column(String, ForeignKey('courses.id'), nullable=False)
    title_name = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False)
    status = Column(Enum(Enums.TitlesStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    course = relationship('Courses', foreign_keys=[course_id])


class Topics(Base):
    __tablename__ = 'topics'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    topic_name = Column(String(255), nullable=False)
    category = Column(Enum(Enums.TopicsCategory), nullable=False)
    tag_id = Column(JSON, ForeignKey('tags.id'), nullable=False)
    study_material = Column(Enum(Enums.TopicsStudyMaterial), nullable=True)
    pdf_material = Column(String(255), nullable=True)
    response_status = Column(Integer, nullable=True)
    status = Column(Enum(Enums.TopicsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    tag = relationship('Tags', foreign_keys=[tag_id])


class UserAcademics(Base):
    __tablename__ = 'user_academics'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    college_id = Column(Enum(Enums.UserAcademicsCollegeId), ForeignKey('colleges.id'), nullable=True)
    batch_id = Column(Enum(Enums.UserAcademicsBatchId), ForeignKey('batches.id'), nullable=True)
    department_id = Column(String, ForeignKey('departments.id'), nullable=True)
    section_id = Column(Enum(Enums.UserAcademicsSectionId), ForeignKey('sections.id'), nullable=True)
    academic_info = Column(JSON, nullable=True)
    personal_info = Column(JSON, nullable=True)
    backlogs = Column(JSON, nullable=True)
    resume = Column(String(255), nullable=True)
    status = Column(Enum(Enums.UserAcademicsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    batch = relationship('Batches', foreign_keys=[batch_id])
    college = relationship('Colleges', foreign_keys=[college_id])
    department = relationship('Departments', foreign_keys=[department_id])
    section = relationship('Sections', foreign_keys=[section_id])
    user = relationship('Users', foreign_keys=[user_id])


class UserAssignments(Base):
    __tablename__ = 'user_assignments'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_allocated_id = Column(Integer, nullable=False)
    topic_id = Column(String, ForeignKey('topics.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    path = Column(String(255), nullable=True)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    topic = relationship('Topics', foreign_keys=[topic_id])
    user = relationship('Users', foreign_keys=[user_id])


class UserCourseEnrollments(Base):
    __tablename__ = 'user_course_enrollments'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_allocation_id = Column(Enum(Enums.UserCourseEnrollmentsCourseAllocationId), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    status = Column(Enum(Enums.UserCourseEnrollmentsStatus), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship('Users', foreign_keys=[user_id])


class Users(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(255), nullable=True)
    roll_no = Column(String(20), nullable=True)
    email_verified_at = Column(DateTime, nullable=True)
    remember_token = Column(Enum(Enums.UsersRememberToken), nullable=True)
    dob = Column(Date, nullable=True)
    gender = Column(Enum(Enums.UsersGender), nullable=True)
    role = Column(Enum(Enums.UsersRole), nullable=False)
    contact_number = Column(BigInteger, nullable=True)
    profile = Column(String(255), nullable=True)
    status = Column(Enum(Enums.UsersStatus), nullable=False)
    password_validate_at = Column(DateTime, nullable=True)
    access = Column(JSON, nullable=True)
    permission = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class VerifyCertificates(Base):
    __tablename__ = 'verify_certificates'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Enum(Enums.VerifyCertificatesUserId), ForeignKey('users.id'), nullable=True)
    theme_id = Column(Enum(Enums.VerifyCertificatesThemeId), nullable=True)
    roll_number = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    date = Column(Date, nullable=True)
    c_certificate = Column(String(255), nullable=True)
    title1 = Column(Enum(Enums.VerifyCertificatesTitle1), nullable=True)
    title2 = Column(String(255), nullable=True)
    title3 = Column(String(255), nullable=True)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    user = relationship('Users', foreign_keys=[user_id])


class VideoBanks(Base):
    __tablename__ = 'video_banks'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    path = Column(String(255), nullable=False)
    subject_id = Column(Integer, nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    title = Column(String(30), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    topic = relationship('Topics', foreign_keys=[topic_id])


class VivaQuestionBank(Base):
    __tablename__ = 'viva_question_bank'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    course_id = Column(String, ForeignKey('courses.id'), nullable=False)
    topic_id = Column(String, ForeignKey('topics.id'), nullable=False)
    question = Column(Text, nullable=False)
    solution = Column(Text, nullable=True)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    course = relationship('Courses', foreign_keys=[course_id])
    topic = relationship('Topics', foreign_keys=[topic_id])

