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
            lines.append("\n### CRITICAL RULES:")
            lines.append("1. Use ONLY the tables and relationships defined below.")
            lines.append("2. Use the EXACT numeric values for Enums (definitions provided).")
            lines.append("3. Return ONLY the SQL query. No markdown, no explanation.")
            
            lines.append("\n### COMPLEX QUERY STRATEGY:")
            lines.append("1. JOIN PATHS: For multi-table questions (e.g. 'Departments in College'), you MUST follow the Relationship Paths defined below. Do not guess foreign keys.")
            lines.append("2. IMPLICIT RELATIONS: We have provided 70+ implicit relationships (e.g. `user_id` -> `users.id`). Use them fearlessly.")
            lines.append("3. ACCURACY: If filtering by status/role, looking up the table below and use the EXACT numeric code (e.g. 'Student' is 7, not 'student').")
            lines.append("4. COURSE ENROLLMENTS: To count students in a course, JOIN `users` -> `course_wise_segregations` -> `courses`. Do NOT use `user_course_enrollments` unless specifically asked. Filter by `users.status=1` ONLY if asked for 'active'.")
            lines.append("5. COLLEGE RESULTS: Result tables are prefixed by college code (e.g., `srec_2025_2_coding_result` for SREC). If the user mentions a college, ALWAYS use their specific `{college}_%_result` table. If it DOES NOT EXIST in the list below, use generic `coding_results` or similar base tables.")
            lines.append("6. TOPIC ANALYSIS: To find topics in a course, JOIN `courses` -> `course_topic_maps` -> `topics`. Use `course_topic_maps.status=1` AND `topics.status=1`.")
            lines.append("7. ASSESSMENT/TEST DATA: For questions about 'assessments', 'tests', or 'how many done':")
            lines.append("   - FIRST check if college-specific `{college}_coding_result` table exists (e.g., `srec_2025_2_coding_result`)")
            lines.append("   - If college-specific table exists, use it: SELECT COUNT(DISTINCT problem_id) FROM {college}_coding_result WHERE user_id = X")
            lines.append("   - If NO college-specific table, use generic tables: `admin_coding_result`, `admin_mcq_result`, `admin_test_data`")
            lines.append("   - For 'my assessments' or 'assessments I done', filter by user_id from the authenticated user")
            lines.append("   - Count DISTINCT problem_id or test_id to avoid duplicates from multiple attempts")


            lines.append("\n### FULL DATABASE SCHEMA (AVAILABLE TABLES ONLY):")
            lines.append("The following tables are CONFIRMED to exist in the database. Do NOT use any table not listed here.")
            
            extracted_relationships = []
            
            for table_name, details in schema['tables'].items():
                # KEY FIX: Only include table if it actually exists in the DB
                if table_name in available_tables:
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
                    # Optional: Log excluded tables to verify logic
                    pass# print(f"Skipping missing table: {table_name}")
            
            lines.append("\n### ENUM INTEL (Use these EXACT values):")
            for table, fields in mappings.items():
                # Only include tables that actually exist in the schema to save tokens
                if table in schema['tables']:
                    lines.append(f"Table `{table}`:")
                    for field, map_data in fields.items():
                        lines.append(f"  - `{field}`: {json.dumps(map_data)}")
            
            lines.append("\n### RELATIONSHIPS (Join Paths):")
            lines.append("Use these paths to join tables:")
            for rel in extracted_relationships:
                lines.append(f"- `{rel['TABLE_NAME']}.{rel['COLUMN_NAME']}` -> `{rel['REFERENCED_TABLE_NAME']}.{rel['REFERENCED_COLUMN_NAME']}`")
                
            self.context_string = "\n".join(lines)
            print("✅ AI Schema Context Loaded (Relationships Extracted from Analysis)")
            
        except Exception as e:
            print(f"❌ Error loading schema context: {e}")
            self.context_string = f"Error loading context: {str(e)}"

    def get_system_prompt(self) -> str:
        return self.context_string

# Singleton
schema_context = SchemaContext()
