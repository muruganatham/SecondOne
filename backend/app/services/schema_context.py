"""
Schema Context Manager
Provides the AI with the "knowledge" of the database structure and Enums.
"""

import json
import os
from datetime import datetime
from app.models.enums import *
from app.core.sql_validator import sql_validator
from app.services.sql_executor import sql_executor


class SchemaContext:
    def __init__(self):
        # Paths
        self.base_path = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.manual_mappings_path = os.path.join(
            self.base_path, "database_analysis", "manual_mappings.json"
        )
        self.complete_schema_path = os.path.join(
            self.base_path, "database_analysis", "complete_schema_analysis.json"
        )

        # Cache
        self.schema_data = {}
        self.mappings = {}
        self.available_tables = set()
        self.context_string = ""  # Basic rules
        self.load_context()

    def load_context(self):
        """Loads the schema metrics into memory but NOT the full string."""
        try:
            # 1. Get Live Tables
            self.available_tables = set(sql_executor.get_available_tables())
            print(f"✅ Schema Context: Found {len(self.available_tables)} tables")

            # 2. Load JSONs
            with open(self.manual_mappings_path, "r", encoding="utf-8") as f:
                self.mappings = json.load(f)

            with open(self.complete_schema_path, "r", encoding="utf-8") as f:
                self.schema_data = json.load(f)

            # 3. Base Rules Prompt (No Tables)
            self.context_string = self.build_rules_prompt()
            print("✅ AI Schema Context Manager Initialized (Smart Retrieval Mode)")

        except Exception as e:
            print(f"❌ Error loading schema context: {e}")
            self.context_string = f"Error loading context: {str(e)}"

    def get_system_prompt(self) -> str:
        return self.context_string

    def get_all_table_names(self) -> str:
        """
        Returns a flat list of ALL available tables with row counts and descriptions.
        Provides the AI with rich context for Stage 1 analysis while keeping tokens relatively low.
        """
        lines = []
        lines.append("DATABASE TABLES (ALL NAMES + CONTEXT):")
        
        # 1. Filter out system/migration tables
        filtered_tables = [
            t for t in self.available_tables 
            if "migration" not in t.lower() and "failed_jobs" not in t.lower()
        ]
        
        # 2. Add as a detailed list
        for t in sorted(filtered_tables):
            details = self.schema_data.get("tables", {}).get(t, {})
            rows = details.get("schema", {}).get("row_count", 0)
            
            # Semantic Hinting based on table name patterns
            context = ""
            if "_coding_result" in t: context = "Student coding test scores and solutions"
            elif "_mcq_result" in t: context = "Student MCQ/Fillup test scores"
            elif "_test_data" in t: context = "Test metadata and settings"
            elif "user_academics" == t: context = "Student academic hierarchy (College, Dept, Batch, Section)"
            elif "users" == t: context = "User profiles, roles, and emails"
            elif "courses" == t: context = "LMS course list and titles"
            elif "topics" == t: context = "Syllabus topics for courses"
            elif "academic_qb" in t: context = "Question bank for academic assessments"
            elif "standard_qb" in t: context = "Standard question bank (coding/mcq)"
            elif "placement" in t: context = "Recruitment and company eligibility data"
            elif "enrollment" in t: context = "Course and student mapping"
            elif "test_question_maps" == t: context = "Bridge between tests and questions"
            elif "tests" == t: context = "Main assessment metadata"
            
            hint = f" | Context: {context}" if context else ""
            lines.append(f"- {t} (Rows: {rows}){hint}")
                
        return "\n".join(lines)

    def get_detailed_schema(self, table_names: list) -> str:
        """
        Extracts FULL JSON schema ONLY for the requested tables.
        This provides the AI with deep context for the chosen tables.
        """
        # 1. Expand wildcards (e.g., 'srec_2025_2_coding_result')
        real_tables = set()
        for name in table_names:
            if name in self.available_tables:
                real_tables.add(name)
            else:
                # fuzzy match?
                pass

        # 2. Smart Table Injection (Core vs. Contextual)
        # Identity tables are universal (always needed for role-based scoping)
        mandatory = {
            "users",
            "user_academics",
            "colleges",
            "departments",
            "batches",
            "sections",
            "courses",
            "course_academic_maps",
        }
        
        # Assessment/Result infrastructure is only added if relevant
        # (e.g., if AI recommended a result table or a test-related table)
        is_assessment_query = any(
            "result" in t.lower() or 
            "test" in t.lower() or 
            "qb" in t.lower() or 
            "segregation" in t.lower() or
            "enrollment" in t.lower()
            for t in real_tables
        )
        
        if is_assessment_query:
            mandatory.update({
                "tests",
                "test_question_maps",
                "standard_qb_codings",
                "standard_qb_mcqs",
                "course_wise_segregations",
                "user_course_enrollments",
                "academic_qb_codings",
                "academic_qb_mcqs"
            })

        real_tables.update(mandatory.intersection(self.available_tables))

        # 3. Build JSON Dump for these tables
        extracted_schema = {"tables": {}}
        for t in real_tables:
            if t in self.schema_data["tables"]:
                raw_table = self.schema_data["tables"][t]
                
                # Simplify Columns
                simple_columns = []
                for col in raw_table.get("schema", {}).get("columns", []):
                    simple_columns.append(
                        f"{col['Field']} ({col['Type']})" + 
                        (f" [PK]" if col['Key'] == 'PRI' else "") +
                        (f" [FK]" if col['Key'] == 'MUL' else "")
                    )

                # Simplify Enums
                simple_enums = {}
                for col, data in raw_table.get("enum_fields", {}).items():
                    # Extract just the values, ignore counts
                    if isinstance(data, dict) and "values" in data:
                        simple_enums[col] = [
                            v["value"] for v in data["values"] 
                            if isinstance(v, dict) and "value" in v
                        ]
                
                extracted_schema["tables"][t] = {
                    "columns": simple_columns,
                    "row_count": raw_table.get("schema", {}).get("row_count", 0),
                    "enums": simple_enums
                }

        # 4. Add Mappings for these tables (keep as is, usually small)
        extracted_mappings = {}
        for t in real_tables:
            if t in self.mappings:
                extracted_mappings[t] = self.mappings[t]

        # 5. Construct Prompt
        lines = []
        lines.append("### SELECTED TABLE SCHEMAS (SIMPLIFIED):")
        lines.append(json.dumps(extracted_schema, indent=2))

        if extracted_mappings:
            lines.append("\n### RELEVANT MANUAL MAPPINGS:")
            lines.append(json.dumps(extracted_mappings, indent=2))

        return "\n".join(lines)



    def build_context_string(self, table_list: list) -> str:
        """Constructs the high-accuracy prompt with specific table columns and Enums"""
        lines = []
        lines.append("You are a MySQL query expert for the 'coderv4' database.")

        lines.append("\n### MANDATORY ACCURACY RULES (CRITICAL):")
        lines.append(
            "1. **STUDENT PROGRESS & RANK**: ALWAYS use `course_wise_segregations`. It contains `progress`, `score`, `rank`, and `performance_rank`. Use these for ANY question about 'how do I compare', 'my rank', or 'average marks'."
        )
        lines.append(
            "2. **ENROLLED COURSES**: Access via `user_course_enrollments` (direct) OR `course_academic_maps` (allocated)."
        )
        lines.append(
            "3. **WPI SCORE**: `(Total_Marks * 0.7) + (Accuracy * 0.2) + (Total_Attempts * 0.1)`."
        )
        lines.append(
            "4. **SOLVED STATUS**: 'Solved' in coding results is `solve_status IN (2, 3)`. 'Fully Solved' is 3."
        )
        lines.append(
            "5. **SUBMISSIONS**: `submission_tracks` (and 2025/2026 variants) contains `code_content` and `error` columns."
        )
        lines.append(
            "6. **MARKETPLACE**: Identification rule: A course is a MARKETPLACE course if in `course_academic_maps`, the fields `college_id`, `department_id`, `batch_id`, and `section_id` are ALL NULL."
        )
        lines.append(
            "7. **FOR STUDENTS**: Every academic query MUST filter by `college_id`, `department_id`, `batch_id`, `section_id` if available in the table. NEVER query academic data outside your assigned IDs."
        )
        lines.append(
            "8. **ENROLLMENT JOIN**: To link direct enrollments to course details, join `user_course_enrollments.course_allocation_id` with `course_academic_maps.id` (NOT directly with `courses`)."
        )
        lines.append(
            "9. **PROGRESS JOIN**: To link your hierarchy to progress data, join `user_academics.user_id` with `course_wise_segregations.user_id`."
        )
        lines.append(
            "10. **FOR ADMINS**: You can query any data across all institutions and departments. Do NOT apply restrictive filters unless explicitly asked by the user."
        )
        lines.append(
            "11. **NO PLACEHOLDERS**: NEVER use `{user_id}` or `:user_id`. Use the literal value provided in the instructions."
        )

        lines.append("\n### GOLDEN JOIN PATHS (USE THESE):")
        lines.append(
            "- **Student Hierarchy**: `users` -> `user_academics` (on user_id) -> `colleges/departments/batches/sections` (on respective ids)"
        )
        lines.append(
            "- **Course Performance**: `users` -> `course_wise_segregations` (on user_id) -> `courses` (on course_id)"
        )
        lines.append(
            "- **Enrollment Strategy**: `user_course_enrollments` -> `course_academic_maps` (on course_allocation_id) -> `courses` (on course_id)"
        )

        if not table_list:
            return "\n".join(lines)

        lines.append("\n### DETAILED TABLE SCHEMAS:")
        included_tables = set()
        blacklist = {"failed_jobs", "otps", "migrations", "shield_logs"}

        for t_name in table_list:
            if (
                t_name in self.available_tables
                and t_name in self.schema_data["tables"]
                and t_name not in blacklist
            ):
                included_tables.add(t_name)
                details = self.schema_data["tables"][t_name]
                columns = [col["Field"] for col in details["schema"]["columns"]]
                lines.append(f"- Table `{t_name}`: Columns({', '.join(columns)})")

                # Add Enums if exist
                if t_name in self.mappings:
                    for field, map_data in self.mappings[t_name].items():
                        lines.append(f"  - Enum `{field}`: {json.dumps(map_data)}")

        lines.append("\n### RELATIONSHIP PATHS (JOIN PATHS):")
        for rel in self.extracted_relationships:
            if (
                rel["TABLE_NAME"] in included_tables
                and rel["REFERENCED_TABLE_NAME"] in included_tables
            ):
                lines.append(
                    f"- `{rel['TABLE_NAME']}.{rel['COLUMN_NAME']}` -> `{rel['REFERENCED_TABLE_NAME']}.{rel['REFERENCED_COLUMN_NAME']}`"
                )

        return "\n".join(lines)

    def build_rules_prompt(self) -> str:
        """Constructs the high-level rules (NO TABLES)."""
        lines = []
        lines.append("You are a MySQL query expert for the 'coderv4' database.")
        lines.append("\n### MANDATORY RULES:")
        lines.append(
            "1. **Analyze First**: Use the provided schema JSON to understand columns and types."
        )
        lines.append(
            "2. **No Hallucinations**: Only use tables provided in the 'SELECTED TABLE SCHEMAS'."
        )
        lines.append(
            "3. **JSON Handling**: Use `JSON_UNQUOTE(JSON_EXTRACT(col, '$.key'))` for JSON fields."
        )
        return "\n".join(lines)


# Singleton
schema_context = SchemaContext()
