import json
import os
import sys
from datetime import datetime
from sqlalchemy import text

# Add backend to path
sys.path.append(os.getcwd())
from app.core.db import SessionLocal

def get_db():
    return SessionLocal()

def regenerate_schema():
    db = get_db()
    print("🚀 Starting Deep Schema Regeneration...")
    
    # 1. Get current database name
    db_name = db.execute(text("SELECT DATABASE()")).scalar()
    print(f"📡 Database: {db_name}")

    # 2. Get all tables
    tables_res = db.execute(text("SHOW TABLES")).fetchall()
    table_names = [t[0] for t in tables_res]
    print(f"📊 Found {len(table_names)} tables")

    schema_data = {
        "database": db_name,
        "analyzed_at": datetime.now().isoformat(),
        "total_tables": len(table_names),
        "tables": {}
    }

    total_relationships = 0

    for t_name in table_names:
        print(f"  🔍 Analyzing table: {t_name}")
        
        try:
            # Get Columns
            cols_res = db.execute(text(f"DESCRIBE `{t_name}`")).fetchall()
            columns = []
            for c in cols_res:
                columns.append({
                    "Field": c[0],
                    "Type": c[1],
                    "Null": c[2],
                    "Key": c[3],
                    "Default": str(c[4]) if c[4] is not None else None,
                    "Extra": c[5]
                })

            # Get Foreign Keys
            fk_query = f"""
            SELECT 
                COLUMN_NAME, 
                REFERENCED_TABLE_NAME, 
                REFERENCED_COLUMN_NAME,
                CONSTRAINT_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
            WHERE TABLE_NAME = '{t_name}'
            AND TABLE_SCHEMA = '{db_name}'
            AND REFERENCED_TABLE_NAME IS NOT NULL
            """
            fks_res = db.execute(text(fk_query)).fetchall()
            fks = []
            for fk in fks_res:
                fks.append({
                    "COLUMN_NAME": fk[0],
                    "REFERENCED_TABLE_NAME": fk[1],
                    "REFERENCED_COLUMN_NAME": fk[2],
                    "CONSTRAINT_NAME": fk[3]
                })
                total_relationships += 1

            # Get Row Count
            try:
                count = db.execute(text(f"SELECT COUNT(*) FROM `{t_name}`")).scalar()
            except:
                count = 0

            schema_data["tables"][t_name] = {
                "schema": {
                    "table_name": t_name,
                    "columns": columns,
                    "row_count": count
                },
                "foreign_keys": fks,
                "purpose": "" 
            }
        except Exception as e:
            print(f"  ❌ Error analyzing table {t_name}: {e}")
            continue

    schema_data["total_relationships"] = total_relationships
    
    # Save back
    output_path = os.path.join("database_analysis", "complete_schema_analysis.json")
    # Ensure dir exists
    os.makedirs("database_analysis", exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schema_data, f, indent=2)
    
    print(f"✅ Regeneration Complete! Processed {len(table_names)} tables and {total_relationships} relationships.")
    print(f"💾 Saved to {output_path}")

if __name__ == "__main__":
    regenerate_schema()
