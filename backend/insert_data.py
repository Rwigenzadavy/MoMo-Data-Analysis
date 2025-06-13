# backend/insert_data.py
import sqlite3
import pandas as pd

def insert_data(csv_path="backend/cleaned_data.csv"):
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect("momo.db")
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO transactions (tx_type, amount, name, datetime, body)
        VALUES (?, ?, ?, ?, ?)
        """, (row["tx_type"], row["amount"], row["name"], row["datetime"], row["body"]))

    conn.commit()
    conn.close()
    print(f"✅ Inserted {len(df)} rows into the database.")

if __name__ == "__main__":
    insert_data()

