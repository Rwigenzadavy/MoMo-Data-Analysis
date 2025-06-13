# backend/db_setup.py
import sqlite3

def create_database():
    conn = sqlite3.connect("momo.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tx_type TEXT,
        amount INTEGER,
        name TEXT,
        datetime TEXT,
        body TEXT
    );
    """)

    conn.commit()
    conn.close()
    print("✅ Database and table created: momo.db")

if __name__ == "__main__":
    create_database()

