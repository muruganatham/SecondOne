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

    def get_schema_summary(self) -> str:
        """
        Returns a summary of ALL available tables for Phase 1 Analysis.
        Dynamically generated from schema data.
        """
        lines = []
        lines.append("AVAILABLE TABLES & METRICS:")

        # Logic to group or list tables
        # for t_name, details in self.schema_data['tables'].items():
        #     if t_name in self.available_tables:
        #         row_count = details['schema'].get('row_count', 0)
        #         lines.append(f"- {t_name} (Rows: {row_count})")

        # Use our curated category list for better semantic understanding
        categories = {
            "Identity": [
                "users",
                "user_academics",
                "colleges",
                "departments",
                "batches",
                "sections",
            ],
            "LMS": [
                "courses",
                "user_course_enrollments",
                "course_academic_maps",
                "course_wise_segregations",
                "topics",
                "sub_topics",
            ],
            "Assessments": [
                "tests",
                "user_assessments",
                "submission_tracks",
                "2025_submission_tracks",
                "2026_submission_tracks",
            ],
            "Questions": [
                "academic_qb_codings",
                "academic_qb_mcqs",
                "standard_qb_codings",
                "standard_qb_mcqs",
            ],
            "Results": [
                "[college]_coding_result",
                "[college]_mcq_result",
            ],  # Generic placeholders
            "Engagement": ["certificates", "discussions", "staff_trainer_feedback"],
        }

        for category, tables in categories.items():
            lines.append(f"\n[{category}]:")
            for t in tables:
                if "[" in t:  # Dynamic placeholder
                    lines.append(
                        f"- {t}: College-specific results (e.g., srec_2025_2_coding_result)"
                    )
                elif t in self.available_tables:
                    details = self.schema_data["tables"].get(t, {})
                    rows = details.get("schema", {}).get("row_count", "?")
                    lines.append(f"- {t} (Rows: {rows})")

        # Add any other large tables not in categories
        lines.append("\n[Others]:")
        known = set(t for cat in categories.values() for t in cat)
        for t_name in sorted(self.available_tables):
            if (
                t_name not in known
                and "failed" not in t_name
                and "migration" not in t_name
            ):
                lines.append(f"- {t_name}")

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

        # 2. Always add Core Tables
        mandatory = {
            "users",
            "user_academics",
            "colleges",
            "departments",
            "course_wise_segregations",
            "courses",
        }
        real_tables.update(mandatory.intersection(self.available_tables))

        # 3. Build JSON Dump for these tables
        extracted_schema = {"tables": {}}
        for t in real_tables:
            if t in self.schema_data["tables"]:
                extracted_schema["tables"][t] = self.schema_data["tables"][t]

        # 4. Add Mappings for these tables
        extracted_mappings = {}
        for t in real_tables:
            if t in self.mappings:
                extracted_mappings[t] = self.mappings[t]

        # 5. Construct Prompt
        lines = []
        lines.append("### SELECTED TABLE SCHEMAS (FULL DEFINITION):")
        lines.append(json.dumps(extracted_schema, indent=2))

        lines.append("\n### RELEVANT ENUM MAPPINGS:")
        lines.append(json.dumps(extracted_mappings, indent=2))

        return "\n".join(lines)

        # Always include identity/hierarchy tables for student-centric JOINs
        mandatory = {
            "users",
            "user_academics",
            "colleges",
            "departments",
            "batches",
            "sections",
            "course_academic_maps",
            "user_course_enrollments",
            "course_wise_segregations",
        }
        target_tables = set(table_names).union(mandatory)
        return self.build_context_string(list(target_tables))

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
