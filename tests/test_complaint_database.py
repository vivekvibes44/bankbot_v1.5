
import sqlite3
from database.db import DB_PATH


def test_complaint_database():
    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.cursor()

        # Verify the previously approved complaint.
        cursor.execute("""
            SELECT complaint_id, category, description, status
            FROM complaints
            WHERE complaint_id = ?
        """, ("RB-C6C7FC48",))

        approved = cursor.fetchall()

        assert len(approved) == 1, (
            "Approved complaint should exist exactly once."
        )

        print("PASS: Approved complaint exists exactly once.")
        print("Approved complaint:", approved[0])

        # Verify the rejected complaint was not saved.
        cursor.execute("""
            SELECT COUNT(*)
            FROM complaints
            WHERE category = ?
              AND description = ?
        """, (
            "Digital Banking",
            "I cannot log in to my mobile banking application."
        ))

        rejected_count = cursor.fetchone()[0]

        assert rejected_count == 0, (
            "Rejected complaint should not exist in the database."
        )

        print("PASS: Rejected complaint was not saved.")

    finally:
        conn.close()


if __name__ == "__main__":
    print("\n========== COMPLAINT DATABASE TESTS ==========\n")

    test_complaint_database()

    print("\n========== ALL TESTS PASSED ==========\n")
