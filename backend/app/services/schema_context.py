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
        Returns a summary of ALL available tables for Phase 1 Analysis.
        Dynamically generated from schema data.
        """
        lines = []
        lines.append("AVAILABLE TABLES AND BRIEF DESCRIPTIONS:")
        
        # Identity & Core (Prioritize these as they are essential for JOINs)
        core_tables = [
            ("users", "Profile, name, email and roles"),
            ("user_academics", "Links students to college, department, batch, section hierarchy"),
            ("colleges", "College information"),
            ("departments", "Department information"),
            ("batches", "Academic batch periods"),
            ("sections", "Class sections")
        ]
        
        for t_name, desc in core_tables:
            if t_name in self.available_tables:
                lines.append(f"- {t_name}: {desc}")

        # LMS Core
        lms_tables = [
            ("courses", "Master list of all courses"),
            ("user_course_enrollments", "Direct mapping of students to courses"),
            ("course_academic_maps", "Hierarchical course allocations to batches/sections"),
            ("course_wise_segregations", "Student progress, scores, and rankings"),
            ("topics", "Course topics/modules"),
            ("sub_topics", "Course sub-topics/lessons")
        ]
        for t_name, desc in lms_tables:
            if t_name in self.available_tables:
                lines.append(f"- {t_name}: {desc}")

        # List EVERYTHING else from the schema data
        lines.append("\nALL OTHER ACCESSIBLE TABLES:")
        
        # Track tables we've already listed
        already_listed = {t[0] for t in core_tables}.union({t[0] for t in lms_tables})
        
        # Sort tables alphabetically for consistent AI consumption
        sorted_tables = sorted(list(self.available_tables))
        
        for t_name in sorted_tables:
            if t_name not in already_listed:
                # Try to get a purpose from schema_data if it exists
                purpose = ""
                try:
                    purpose = self.schema_data.get('tables', {}).get(t_name, {}).get('purpose', "")
                except: pass
                
                if purpose:
                    lines.append(f"- {t_name}: {purpose}")
                else:
                    # Fallback to column-based purpose if possible, or just the name
                    lines.append(f"- {t_name}")
        
        lines.append("\nINSTRUCTIONS FOR ANALYSIS:")
        lines.append("1. Search this entire list for tables that might contain the requested data.")
        lines.append("2. Consider both direct links (e.g. user_id in table) and hierarchical links (e.g. table linked to batch/section/college).")
        lines.append("3. If data is about enrollment, check BOTH user_course_enrollments and course_academic_maps.")
        
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
        lines.append("1. **STUDENT PROGRESS & RANK**: ALWAYS use `course_wise_segregations`. It contains `progress`, `score`, `rank`, and `performance_rank`. Use these for ANY question about 'how do I compare', 'my rank', or 'average marks'.")
        lines.append("2. **ENROLLED COURSES**: Access via `user_course_enrollments` (direct) OR `course_academic_maps` (allocated).")
        lines.append("3. **WPI SCORE**: `(Total_Marks * 0.7) + (Accuracy * 0.2) + (Total_Attempts * 0.1)`.")
        lines.append("4. **SOLVED STATUS**: 'Solved' in coding results is `solve_status IN (2, 3)`. 'Fully Solved' is 3.")
        lines.append("5. **SUBMISSIONS**: `submission_tracks` (and 2025/2026 variants) contains `code_content` and `error` columns.")
        lines.append("6. **MARKETPLACE**: Identification rule: A course is a MARKETPLACE course if in `course_academic_maps`, the fields `college_id`, `department_id`, `batch_id`, and `section_id` are ALL NULL.")
        lines.append("7. **FOR STUDENTS**: Every academic query MUST filter by `college_id`, `department_id`, `batch_id`, `section_id` if available in the table. NEVER query academic data outside your assigned IDs.")
        lines.append("8. **ENROLLMENT JOIN**: To link direct enrollments to course details, join `user_course_enrollments.course_allocation_id` with `course_academic_maps.id` (NOT directly with `courses`).")
        lines.append("9. **PROGRESS JOIN**: To link your hierarchy to progress data, join `user_academics.user_id` with `course_wise_segregations.user_id`.")
        lines.append("10. **FOR ADMINS**: You can query any data across all institutions and departments. Do NOT apply restrictive filters unless explicitly asked by the user.")
        lines.append("11. **NO PLACEHOLDERS**: NEVER use `{user_id}` or `:user_id`. Use the literal value provided in the instructions.")
        
        lines.append("\n### GOLDEN JOIN PATHS (USE THESE):")
        lines.append("- **Student Hierarchy**: `users` -> `user_academics` (on user_id) -> `colleges/departments/batches/sections` (on respective ids)")
        lines.append("- **Course Performance**: `users` -> `course_wise_segregations` (on user_id) -> `courses` (on course_id)")
        lines.append("- **Enrollment Strategy**: `user_course_enrollments` -> `course_academic_maps` (on course_allocation_id) -> `courses` (on course_id)")

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