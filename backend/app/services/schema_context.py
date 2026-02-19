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
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.manual_mappings_path = os.path.join(self.base_path, "database_analysis", "manual_mappings.json")
        self.complete_schema_path = os.path.join(self.base_path, "database_analysis", "complete_schema_analysis.json")
        
        # Cache
        self.schema_data = {}
        self.mappings = {}
        self.available_tables = set()
        self.context_string = "" # Basic rules
        self.load_context()

    def load_context(self):
        """Loads the schema metrics into memory but NOT the full string."""
        try:
            # 1. Get Live Tables
            self.available_tables = set(sql_executor.get_available_tables())
            print(f"✅ Schema Context: Found {len(self.available_tables)} tables")

            # 2. Load JSONs
            with open(self.manual_mappings_path, 'r', encoding='utf-8') as f:
                self.mappings = json.load(f)
                
            with open(self.complete_schema_path, 'r', encoding='utf-8') as f:
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
        Returns a LIGHTWEIGHT summary of all tables for the 'Analysis' phase.
        Format: - table_name (Rows: N) [Description if available]
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
            "Identity": ["users", "user_academics", "colleges", "departments", "batches", "sections"],
            "LMS": ["courses", "user_course_enrollments", "course_academic_maps", "course_wise_segregations", "topics", "sub_topics"],
            "Assessments": ["tests", "user_assessments", "submission_tracks", "2025_submission_tracks", "2026_submission_tracks"],
            "Questions": ["academic_qb_codings", "academic_qb_mcqs", "standard_qb_codings", "standard_qb_mcqs"],
            "Results": ["[college]_coding_result", "[college]_mcq_result"], # Generic placeholders
            "Engagement": ["certificates", "discussions", "staff_trainer_feedback"]
        }
        
        for category, tables in categories.items():
            lines.append(f"\n[{category}]:")
            for t in tables:
                if "[" in t: # Dynamic placeholder
                     lines.append(f"- {t}: College-specific results (e.g., srec_2025_2_coding_result)")
                elif t in self.available_tables:
                     details = self.schema_data['tables'].get(t, {})
                     rows = details.get('schema', {}).get('row_count', '?')
                     lines.append(f"- {t} (Rows: {rows})")
        
        # Add any other large tables not in categories
        lines.append("\n[Others]:")
        known = set(t for cat in categories.values() for t in cat)
        for t_name in sorted(self.available_tables):
            if t_name not in known and "failed" not in t_name and "migration" not in t_name:
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
        mandatory = {"users", "user_academics", "colleges", "departments", "course_wise_segregations", "courses"}
        real_tables.update(mandatory.intersection(self.available_tables))
        
        # 3. Build JSON Dump for these tables
        extracted_schema = {"tables": {}}
        for t in real_tables:
            if t in self.schema_data['tables']:
                extracted_schema['tables'][t] = self.schema_data['tables'][t]
                
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

    def build_rules_prompt(self) -> str:
        """Constructs the high-level rules (NO TABLES)."""
        lines = []
        lines.append("You are a MySQL query expert for the 'coderv4' database.")
        lines.append("\n### MANDATORY RULES:")
        lines.append("1. **Analyze First**: Use the provided schema JSON to understand columns and types.")
        lines.append("2. **No Hallucinations**: Only use tables provided in the 'SELECTED TABLE SCHEMAS'.")
        lines.append("3. **JSON Handling**: Use `JSON_UNQUOTE(JSON_EXTRACT(col, '$.key'))` for JSON fields.")
        return "\n".join(lines)

# Singleton
schema_context = SchemaContext()
