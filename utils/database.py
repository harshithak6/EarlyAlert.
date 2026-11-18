
import sqlite3
import os

DATABASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "earlyalert.db"
)


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Store student risk analysis
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risk_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            risk_score INTEGER,
            risk_level TEXT,
            reasons TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Store AI explanations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS explanations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Store mentor communication and approval
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mentor_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            message TEXT,
            meeting_slot TEXT,
            approved INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_risk_record(student):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO risk_records
        (student_id, risk_score, risk_level, reasons)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM risk_records
            WHERE student_id = ?
        )
    """, (
        student["student_id"],
        student["score"],
        student["level"],
        "; ".join(student["reasons"]),
        student["student_id"]
    ))

    connection.commit()
    connection.close()



def save_explanation(student_id, explanation):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO explanations (student_id, explanation)
        VALUES (?, ?)
    """, (student_id, explanation))

    connection.commit()
    connection.close()


def save_mentor_record(student_id, message, meeting_slot, approved):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO mentor_records
        (student_id, message, meeting_slot, approved)
        VALUES (?, ?, ?, ?)
    """, (student_id, message, meeting_slot, int(approved)))

    connection.commit()
    connection.close()
