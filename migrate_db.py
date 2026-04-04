from database import engine
from sqlalchemy import text

def run_migration():
    with engine.connect() as conn:
        try:
            # Check if column exists, if not add it
            conn.execute(text("ALTER TABLE users ADD COLUMN saved_address VARCHAR(255) DEFAULT '';"))
            conn.commit()
            print("Successfully added saved_address to users table.")
        except Exception as e:
            # If the column already exists, this will raise an OperationalError, which is fine to catch and ignore.
            if 'Duplicate column name' in str(e):
                print("Column saved_address already exists.")
            else:
                print(f"Error applying migration: {e}")

if __name__ == "__main__":
    run_migration()
