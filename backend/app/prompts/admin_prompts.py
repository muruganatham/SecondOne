def get_admin_prompt() -> str:
    """
    Returns the system prompt for Super Admin (1) and Admin (2).
    """
    return """
    \n\n[SECURITY PROTOCOL: SUPER ADMIN / ADMIN LEVEL]
    USER CONTEXT: System Administrator with UNRESTRICTED ACCESS.
    
    PERMISSIONS:
    1. ALLOWED: **GLOBAL VIEW**.
       - Can access ALL tables, ALL users, and ALL data across Colleges.
       - Example: "Show overall user data", "List all staff in the system".
       
    RESTRICTIONS:
    - NONE.
    """
