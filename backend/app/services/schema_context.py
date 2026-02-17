"""
Schema Context Manager
Provides the AI with the "knowledge" of the database structure and Enums.
"""
import json
import os
from app.models.enums import * # Import all enums to introspect them if needed, or rely on JSON
from app.services.sql_executor import sql_executor  # Import SQLExecutor to check DB

class SchemaContext:
    def __init__(self):
        # Load the 100% accurate artifacts we generated
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.manual_mappings_path = os.path.join(self.base_path, "database_analysis", "manual_mappings.json")
        # relationships.json is deprecated/redundant; we extract from complete_schema_analysis.json
        self.complete_schema_path = os.path.join(self.base_path, "database_analysis", "complete_schema_analysis.json")
        
        # Cache
        self.context_string = ""
        self.load_context()

    def load_context(self):
        """Loads and formats the schema context for the AI, filtering for EXISTING tables only"""
        try:
            # 1. Get Live Tables from DB
            available_tables = set(sql_executor.get_available_tables())
            print(f"✅ Schema Context: Found {len(available_tables)} available tables in DB")

            with open(self.manual_mappings_path, 'r', encoding='utf-8') as f:
                mappings = json.load(f)
                
            with open(self.complete_schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
                
            # Build the prompt
            lines = []
            lines.append("You are a MySQL query expert. Your goal is to convert user questions into VALID SQL for the 'coderv4' database.")
            lines.append("\n### MANDATORY ACCURACY RULES (CRITICAL):")
            lines.append("1. **ENROLLED COURSES**: To count courses, you MUST use `course_academic_maps` (CAM). Use `COUNT(DISTINCT course_id)`. Joint with `user_academics` to filter by the user's circle (College, Dept, Batch, Section).")
            lines.append("2. **FORBIDDEN TABLES**: NEVER use `course_wise_segregations` for course counts; it is inaccurate and contains outdated data.")
            lines.append("3. **WPI SCORE**: Formula = `(Total_Marks * 0.7) + (Accuracy * 0.2) + (Total_Attempts * 0.1)`.")
            lines.append("4. **ACCURACY**: Formula = `(Solved_Count * 100.0) / Total_Attempts`.")
            lines.append("5. **SECURITY BOUNDARY**: Every query for student analytics MUST filter by `college_id`, `department_id`, `batch_id`, and `section_id` to ensure isolation.")

            lines.append("\n### COMPLEX QUERY STRATEGY:")
            lines.append("1. JOIN PATHS: For multi-table questions, follow the Relationship Paths defined below. Do not guess foreign keys.")
            lines.append("2. IMPLICIT RELATIONS: Use the provided 70+ implicit relationships fearlessly.")
            lines.append("3. ACCURACY: If filtering by status/role, use the EXACT numeric code (e.g. 'Student' is 7).")
            lines.append("4. COLLEGE RESULTS: Result tables are prefixed by college code (e.g., `srec_..._result`). Use them if they exist in the schema below.")
            lines.append("5. TOPIC ANALYSIS: Link Results -> Questions -> Topics via the appropriate QB tables.")
            lines.append("6. ASSESSMENT DATA: Count DISTINCT problem_id or test_id to avoid duplicates.")


            lines.append("\n### SOLVE STATUS MAPPING (IMPORTANT):")
            lines.append("To count 'Solved' questions in `admin_coding_result` or `{college}_coding_result`:")
            lines.append("- ALWAYS use `solve_status IN (2, 3)` for 'Solved' or 'Success'.")
            lines.append("- `solve_status = 2` = Solved/Partially Solved.")
            lines.append("- `solve_status = 3` = Fully Solved.")
            lines.append("- Count DISTINCT `question_id` (or `problem_id`) to get the unique solved count.")

            lines.append("\n### SYSTEM ARCHITECTURE (FEATURE MAPPING):")
            lines.append("The 163+ tables are organized into 10 functional modules. Refer to these to find logic blocks:")
            lines.append("1. USER IDENTITY: `users`, `otps`, `user_login_activities` (Role IDs 1-7).")
            lines.append("2. HIERARCHY: `institutions`, `colleges`, `departments`, `batches`, `sections`.")
            lines.append("3. QUESTION BANK: Standard (`standard_qb_...`) & Academic (`academic_qb_...`). Supports MCQ, Coding, Projects, Viva.")
            lines.append("4. LMS: `courses`, `topics`, `video_banks`, `study_material_banks` (Linked via `course_topic_maps`).")
            lines.append("5. ASSESSMENT ENGINE: `tests`, `test_modules`, `testpage_user_tracks`.")
            lines.append("6. ANALYTICS (RESULTS): College-specific (e.g., `srec_..._result`) and Global (`admin_..._result`).")
            lines.append("7. CERTIFICATION: `certificates`, `verify_certificates`.")
            lines.append("8. COMMUNICATION: `discussions`, `feedback_questions`, `staff_trainer_feedback`.")
            lines.append("9. AI POWERED: `a_i_high_lights`, `ai_prompts` (Use for summaries and insights).")
            lines.append("10. OPERATIONS: `shield_logs`, `audits`, `failed_jobs`.")

            lines.append("\n### FULL DATABASE SCHEMA (AVAILABLE TABLES ONLY):")
            lines.append("The following tables are CONFIRMED to exist in the database. Do NOT use any table not listed here.")
            
            extracted_relationships = []
            
            # 1.5 Define Blacklist (Tables the AI should NEVER see or use)
            blacklist = {"course_wise_segregations", "shield_logs", "failed_jobs", "otps", "migrations"}

            for table_name, details in schema['tables'].items():
                # KEY FIX: Only include table if it actually exists AND is not blacklisted
                if table_name in available_tables and table_name not in blacklist:
                    columns = [col['Field'] for col in details['schema']['columns']]
                    lines.append(f"- Table `{table_name}`: Columns({', '.join(columns)})")
                    
                    # Extract Relationships on the fly
                    fks = details.get('foreign_keys', [])
                    for fk in fks:
                        extracted_relationships.append({
                            'TABLE_NAME': table_name,
                            'COLUMN_NAME': fk['COLUMN_NAME'],
                            'REFERENCED_TABLE_NAME': fk['REFERENCED_TABLE_NAME'],
                            'REFERENCED_COLUMN_NAME': fk['REFERENCED_COLUMN_NAME']
                        })
                else:
                    # Tables missing or filtered out
                    pass

            lines.append("\n### ENUM INTEL (Use these EXACT values):")
            for table, fields in mappings.items():
                if table in schema['tables'] and table not in blacklist:
                    lines.append(f"Table `{table}`:")
                    for field, map_data in fields.items():
                        lines.append(f"  - `{field}`: {json.dumps(map_data)}")
            
            lines.append("\n### RELATIONSHIPS (Join Paths):")
            lines.append("Use these paths to join tables:")
            for rel in extracted_relationships:
                lines.append(f"- `{rel['TABLE_NAME']}.{rel['COLUMN_NAME']}` -> `{rel['REFERENCED_TABLE_NAME']}.{rel['REFERENCED_COLUMN_NAME']}`")
                
            lines.append("\n### MANDATORY ACCURACY RULES (CRITICAL):")
            lines.append("1. **ENROLLED COURSES**: To count courses, you MUST use `course_academic_maps` (CAM). Use `COUNT(DISTINCT course_id)`. Join with `user_academics` to filter by the user's circle (College, Dept, Batch, Section).")
            lines.append("2. **FORBIDDEN TABLES**: NEVER use `course_wise_segregations` for course counts; it is inaccurate and contains outdated data.")
            lines.append("3. **WPI SCORE**: Formula = `(Total_Marks * 0.7) + (Accuracy * 0.2) + (Total_Attempts * 0.1)`.")
            lines.append("4. **ACCURACY**: Formula = `(Solved_Count * 100.0) / Total_Attempts`.")
            lines.append("5. **SECURITY BOUNDARY**: Every query for student analytics MUST filter by `college_id`, `department_id`, `batch_id`, and `section_id` to ensure isolation.")

            self.context_string = "\n".join(lines)
            print("✅ AI Schema Context Loaded (Accuracy Rules At Bottom)")
            
        except Exception as e:
            print(f"❌ Error loading schema context: {e}")
            self.context_string = f"Error loading context: {str(e)}"

    def get_system_prompt(self) -> str:
        return self.context_string

# Singleton
schema_context = SchemaContext()
