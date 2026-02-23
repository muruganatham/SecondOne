
import sys
import os

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(os.path.join(os.getcwd(), "backend"))

try:
    from app.core.config import settings
    from app.services.ai_service import AIService

    print("--- Configuration Verification ---")
    print(f"MAX_TOKEN_LIMIT (Context): {settings.MAX_TOKEN_LIMIT}")
    print(f"AI_MAX_OUTPUT_TOKENS (Output): {getattr(settings, 'AI_MAX_OUTPUT_TOKENS', 'NOT FOUND')}")

    service = AIService()
    print("\n--- Service Inspection ---")
    print("AIService initialized successfully.")

    # We can't easily inspect the method code at runtime without using `inspect`, 
    # but successful import means the usage of settings.AI_MAX_OUTPUT_TOKENS didn't cause a NameError/AttributeError at module level (if it was used in default args, but it's used inside methods).
    
    print("\n✅ Configuration loaded and service instantiated.")

except Exception as e:
    print(f"\n❌ Verification Failed: {e}")
    import traceback
    traceback.print_exc()
