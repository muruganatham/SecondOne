import os
import sys
from unittest.mock import MagicMock

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.ai_service import ai_service
from app.services.schema_context import schema_context
from app.models.profile_models import UserAcademics

# Mock Objects to simulate FastAPI Dependency Injection
class MockUser:
    def __init__(self, id, role):
        self.id = id
        self.role = role

def get_role_instruction(user):
    # Replicating logic from ai_query.py for verification
    if user.role == 1: # Super Admin
        return f"\n\n[ROLE: SUPER ADMIN]\nAccess Level: UNRESTRICTED.\nContext: You are the root administrator. You have full access to all tables and records. You can query any user, college, or department without restriction."
    
    elif user.role == 3: # College Admin
        # Mocking college ID directly for test
        college_id = 999 
        return f"\n\n[ROLE: COLLEGE ADMIN]\nAccess Level: RESTRICTED (College Scope).\nContext: You manage College ID '{college_id}'.\nCRITICAL RULES:\n1. You MUST append \"WHERE college_id = '{college_id}'\" to ANY query involving 'users', 'students', 'departments', 'academics', or related tables.\n2. Do NOT show data from other colleges."
            
    else: # Student
        return f"\n\n[ROLE: STUDENT/USER]\nAccess Level: RESTRICTED (Personal Scope).\nContext: You are User ID '{user.id}'.\nCRITICAL RULES:\n1. You can ONLY see your own data.\n2. For the 'users' table, you must use \"WHERE id = '{user.id}'\".\n3. For linked tables (academics, results, chats), you must use \"WHERE user_id = '{user.id}'\".\n4. You CANNOT query aggregates (COUNT, AVG) across the database unless scoped strictly to yourself."

def run_test():
    print("=== RBAC VERIFICATION TEST ===\n")
    
    # 1. Test Super Admin
    admin_user = MockUser(id="admin_1", role=1)
    prompt_admin = schema_context.get_system_prompt() + get_role_instruction(admin_user)
    
    print("Test 1: Super Admin asking 'Count all users'")
    try:
        sql_admin = ai_service.generate_sql(prompt_admin, "Count all users", "deepseek-chat")
        print(f"Generated SQL: {sql_admin}")
        if "WHERE" not in sql_admin or "WHERE id =" not in sql_admin:
             print("Result: PASS (No strict filtering applied)")
        else:
             print("Result: WARN (Filtering applied, might be intentional but unexpected for Super Admin)")
    except Exception as e:
        print(f"Error calling LLM: {e}")

    print("\n" + "-"*50 + "\n")

    # 2. Test Student
    student_user = MockUser(id="student_123", role=5)
    prompt_student = schema_context.get_system_prompt() + get_role_instruction(student_user)
    
    print("Test 2: Student asking 'Count all users'")
    try:
        sql_student = ai_service.generate_sql(prompt_student, "Count all users", "deepseek-chat")
        print(f"Generated SQL: {sql_student}")
        if "WHERE" in sql_student and ("id = 'student_123'" in sql_student or "user_id = 'student_123'" in sql_student):
             print("Result: PASS (Strict filtering applied)")
        else:
             print("Result: FAIL (Student was able to query global data!)")
    except Exception as e:
        print(f"Error calling LLM: {e}")

if __name__ == "__main__":
    run_test()
