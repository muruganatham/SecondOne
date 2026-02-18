"""
Schema Context Manager
Provides the AI with the "knowledge" of the database structure and Enums.
"""
import json
import os
from datetime import datetime
from app.models.enums import * 
from app.services.sql_executor import sql_executor

class SchemaContext:
    def __init__(self):
        # Paths
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.manual_mappings_path = os.path.join(self.base_path, "database_analysis", "manual_mappings.json")
        self.complete_schema_path = os.path.join(self.base_path, "database_analysis", "complete_schema_analysis.json")
        
        # Cache
        self.context_string = ""
        self.extracted_relationships = []
        self.available_tables = set()
        self.schema_data = {}
        self.load_context()

    def load_context(self):
        """Loads and formats the schema context for the AI, filtering for EXISTING tables only"""
        try:
            # 1. Get Live Tables from DB
            self.available_tables = set(sql_executor.get_available_tables())
            print(f"✅ Schema Context: Found {len(self.available_tables)} available tables in DB")

            # 2. Load Mapping and Schema Meta
            with open(self.manual_mappings_path, 'r', encoding='utf-8') as f:
                self.mappings = json.load(f)
                
            with open(self.complete_schema_path, 'r', encoding='utf-8') as f:
                self.schema_data = json.load(f)
            
            # 3. Pre-extract relationships for speed
            self.extracted_relationships = []
            for t_name, details in self.schema_data['tables'].items():
                if t_name in self.available_tables:
                    for fk in details.get('foreign_keys', []):
                        self.extracted_relationships.append({
                            'TABLE_NAME': t_name,
                            'COLUMN_NAME': fk['COLUMN_NAME'],
                            'REFERENCED_TABLE_NAME': fk['REFERENCED_TABLE_NAME'],
                            'REFERENCED_COLUMN_NAME': fk['REFERENCED_COLUMN_NAME']
                        })

            # 4. Set default system prompt (Rules Only, no tables by default for token efficiency)
            self.context_string = self.build_context_string([])
            print("✅ AI Schema Context Manager Initialized (Two-Step Optimization Active)")
            
        except Exception as e:
            print(f"❌ Error loading schema context: {e}")
            self.context_string = f"Error loading context: {str(e)}"

    def get_system_prompt(self) -> str:
        return self.context_string

    def get_schema_summary(self) -> str:
        """
        Returns a summary of tables for Phase 1 Analysis.
        """
        lines = []
        lines.append("AVAILABLE TABLES AND DESCRIPTIONS:")
        
        # Identity
        lines.append("- users: Profile, name, email and roles (Student role_id=7)")
        lines.append("- user_academics: Links students to college_id, department_id, batch_id, section_id")
        lines.append("- colleges, departments, batches, sections: Institutional hierarchy")
        
        # LMS & Progress
        lines.append("- courses: Master list of all academic and local courses")
        lines.append("- user_course_enrollments: Direct mapping of students to courses")
        lines.append("- course_academic_maps: Group-based course allocations to batches/sections")
        lines.append("- course_wise_segregations: PRIMARY table for student PROGRESS, scores, and rankings")
        lines.append("- topics, sub_topics: Course content hierarchy")
        lines.append("- academic_study_material_banks, video_banks: PDF and Video lesson files")
        
        # Marketplace & Global Courses
        lines.append("- course_academic_maps: Marketplace courses are those where college_id, department_id, batch_id, and section_id are ALL NULL.")
        lines.append("- standard_qb_courses: Catalog of standard/standard question bank courses")
        lines.append("- standard_qb_topics: Topics for standard courses")
        lines.append("- package_billings: Student purchase history and marketplace orders")
        
        # Assessments
        lines.append("- tests, test_modules: Exam metadata and definitions")
        lines.append("- standard_qb_codings, academic_qb_codings: Coding question pools")
        lines.append("- standard_qb_mcqs, academic_qb_mcqs: MCQ question pools")
        lines.append("- user_assessments: Record of test attempts and solved status (DO NOT CONFUSE WITH PROGRESS)")
        lines.append("- submission_tracks, 2025_submission_tracks: Student submitted code content and execution errors")
        
        # Results
        lines.append("- admin_coding_result, admin_mcq_result: Global student performance marks")
        lines.append("- [college_short_name]_coding_result: Local student result (e.g. srec_2025_2_coding_result)")
        lines.append("- placed_students: Placement company name, packages and status")
        
        # Engagement
        lines.append("- verify_certificates: List of earned student certificates")
        lines.append("- academic_qb_projects: Assigned student projects and tasks")
        lines.append("- course_staff_trainer_allocations: PRIMARY table for trainer/staff assignments to batches/sections")
        lines.append("- staff_trainer_feedback: Student ratings for trainers")
        lines.append("- discussions: Community Q&A forum posts")
        
        return "\n".join(lines)

    def get_detailed_schema(self, table_names: list) -> str:
        """
        Generates detailed schema ONLY for requested tables to save tokens.
        """
        # Always include identity/hierarchy tables for student-centric JOINs
        mandatory = {
            "users", "user_academics", "colleges", "departments", "batches", "sections",
            "course_academic_maps", "user_course_enrollments", "course_wise_segregations"
        }
        target_tables = set(table_names).union(mandatory)
        return self.build_context_string(list(target_tables))

    def build_context_string(self, table_list: list) -> str:
        """Constructs the high-accuracy prompt with specific table columns and Enums"""
        lines = []
        lines.append("You are a MySQL query expert for the 'coderv4' database.")
        
        lines.append("\n### MANDATORY ACCURACY RULES (CRITICAL):")
        lines.append("1. **STUDENT PROGRESS**: ALWAYS use `course_wise_segregations`. It contains `progress` (decimal) and `score`.")
        lines.append("2. **ENROLLED COURSES**: Access via `user_course_enrollments` (direct) OR `course_academic_maps` (allocated).")
        lines.append("3. **WPI SCORE**: `(Total_Marks * 0.7) + (Accuracy * 0.2) + (Total_Attempts * 0.1)`.")
        lines.append("4. **SOLVED STATUS**: 'Solved' in coding results is `solve_status IN (2, 3)`. 'Fully Solved' is 3.")
        lines.append("5. **SUBMISSIONS**: `submission_tracks` (and 2025/2026 variants) contains `code_content` and `error` columns.")
        lines.append("6. **MARKETPLACE**: Identification rule: A course is a MARKETPLACE course if in `course_academic_maps`, the fields `college_id`, `department_id`, `batch_id`, and `section_id` are ALL NULL.")
        lines.append("7. **FOR STUDENTS**: Every academic query MUST filter by `college_id`, `department_id`, `batch_id`, `section_id` if available in the table. NEVER query academic data outside your assigned IDs.")
        lines.append("8. **FOR ADMINS**: You can query any data across all institutions and departments. Do NOT apply restrictive filters unless explicitly asked by the user.")
        lines.append("9. **NO PLACEHOLDERS**: NEVER use `{user_id}` or `:user_id`. Use the literal value provided in the instructions.")

        if not table_list:
            return "\n".join(lines)

        lines.append("\n### DETAILED TABLE SCHEMAS:")
        included_tables = set()
        blacklist = {"failed_jobs", "otps", "migrations", "shield_logs"}

        for t_name in table_list:
            if t_name in self.available_tables and t_name in self.schema_data['tables'] and t_name not in blacklist:
                included_tables.add(t_name)
                details = self.schema_data['tables'][t_name]
                columns = [col['Field'] for col in details['schema']['columns']]
                lines.append(f"- Table `{t_name}`: Columns({', '.join(columns)})")
                
                # Add Enums if exist
                if t_name in self.mappings:
                    for field, map_data in self.mappings[t_name].items():
                        lines.append(f"  - Enum `{field}`: {json.dumps(map_data)}")

        lines.append("\n### RELATIONSHIP PATHS (JOIN PATHS):")
        for rel in self.extracted_relationships:
            if rel['TABLE_NAME'] in included_tables and rel['REFERENCED_TABLE_NAME'] in included_tables:
                lines.append(f"- `{rel['TABLE_NAME']}.{rel['COLUMN_NAME']}` -> `{rel['REFERENCED_TABLE_NAME']}.{rel['REFERENCED_COLUMN_NAME']}`")
        
        return "\n".join(lines)

# Singleton
schema_context = SchemaContext()
