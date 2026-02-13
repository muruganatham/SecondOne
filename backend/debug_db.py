from app.core.config import settings
from sqlalchemy import create_engine, text
import os

def debug_db():
    print(f"Host: {settings.DB_HOST}")
    print(f"Port: {settings.DB_PORT}")
    print(f"User: {settings.DB_USER}")
    print(f"DB: {settings.DB_NAME}")
    
    connect_args = {}
    # Simulate the logic in db.py
    ca_path = "/etc/ssl/certs/ca-certificates.crt"
    if os.path.exists(ca_path):
        connect_args["ssl"] = {"ca": ca_path}
    else:
        # On Windows, we might need a specific certificate or just ssl=True
        connect_args["ssl"] = {}
        print("Using empty ssl dict (Windows fallback)")

    url = settings.DATABASE_URL
    print(f"URL: {url.split('@')[1]}") # Print only host part for safety
    
    try:
        engine = create_engine(url, connect_args=connect_args)
        with engine.connect() as conn:
            res = conn.execute(text("SHOW TABLES"))
            tables = res.fetchall()
            print(f"✅ Success! Found {len(tables)} tables.")
            for t in tables[:5]:
                print(f" - {t[0]}")
    except Exception as e:
        print(f"❌ Connection Failed: {type(e).__name__}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    debug_db()
