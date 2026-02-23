
import sys
import os

# Add current directory to path so we can import 'app'
sys.path.append(os.getcwd())

try:
    from app.core.config import settings
    # context check
    print(f"MAX_TOKEN_LIMIT: {settings.MAX_TOKEN_LIMIT}")
    print(f"AI_MAX_OUTPUT_TOKENS: {getattr(settings, 'AI_MAX_OUTPUT_TOKENS', 'NOT FOUND')}")
    
    # Import service to check for syntax errors or import issues
    from app.services.ai_service import AIService
    print("AIService imported successfully")

except Exception as e:
    print(f"Error: {e}")
