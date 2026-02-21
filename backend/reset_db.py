import sqlite3
import os
from app.doctors_store import init_db, DB_PATH

def reset_database():
    print(f"Checking for database at: {DB_PATH}")
    CSV_PATH = "static/assessments_history.csv"
    if os.path.exists(CSV_PATH):
        try:
            os.remove(CSV_PATH)
            print("Successfully deleted assessment history CSV.")
        except Exception as e:
            print(f"Error deleting CSV: {e}")

    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print("Successfully deleted existing database.")
        except Exception as e:
            print(f"Error deleting database: {e}")
    else:
        print("No database found to delete.")

    print("Re-initializing database...")
    init_db()
    
    # Optional: Verify the schema
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(patients)")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    
    print(f"Table 'patients' columns: {columns}")
    if 'email' in columns:
        print("Success: 'email' column detected.")
    else:
        print("Error: 'email' column missing!")

if __name__ == "__main__":
    reset_database()
