
import csv
import sqlite3

CSV_FILE = "data/student_academic_data.csv"
DB_FILE = "utils/earlyalert.db"

# Read student IDs and names from CSV
student_names = {}

with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        student_names[row["student_id"]] = row["student_name"]

# Connect to SQLite
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

tables = ["risk_records", "explanations", "mentor_records"]

for table in tables:
    columns = [
        row[1]
        for row in cursor.execute(f"PRAGMA table_info({table})")
    ]

    # Add student_name column if it doesn't exist
    if "student_name" not in columns:
        cursor.execute(
            f"ALTER TABLE {table} ADD COLUMN student_name TEXT"
        )

    # Update student names using student IDs
    for student_id, student_name in student_names.items():
        cursor.execute(
            f"""
            UPDATE {table}
            SET student_name = ?
            WHERE student_id = ?
            """,
            (student_name, student_id)
        )

conn.commit()
conn.close()

print("Database updated successfully!")

for table in tables:
    print(f"{table}: student_name column added/updated")
