
import uuid

from database.db import get_connection


# Allowed complaint categories
VALID_CATEGORIES = [
    "Account Services",
    "Debit Card",
    "Digital Banking",
    "Loan Services",
    "Transactions",
    "Other"
]

# Allowed complaint statuses
VALID_STATUSES = [
    "Open",
    "In Progress",
    "Resolved"
]


def register_complaint(category: str, description: str):
    """
    Register a new simulated banking complaint.
    """

    category = category.strip()
    description = description.strip()

    if category not in VALID_CATEGORIES:
        raise ValueError("Invalid complaint category.")

    if not description:
        raise ValueError("Complaint description cannot be empty.")

    # Generate unique complaint ID
    complaint_id = f"RB-{uuid.uuid4().hex[:8].upper()}"

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO complaints (
                complaint_id,
                category,
                description
            )
            VALUES (?, ?, ?)
        """, (complaint_id, category, description))

        connection.commit()

        return {
            "status": "success",
            "complaint_id": complaint_id,
            "category": category,
            "description": description,
            "complaint_status": "Open",
            "message": "Complaint registered successfully."
        }

    finally:
        connection.close()


def get_complaint(complaint_id: str):
    """
    Retrieve a complaint using its unique ID.
    """

    complaint_id = complaint_id.strip().upper()

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM complaints
            WHERE complaint_id = ?
        """, (complaint_id,))

        complaint = cursor.fetchone()

        if complaint is None:
            return {
                "status": "not_found",
                "message": "No complaint found with this ID."
            }

        return {
            "status": "success",
            "complaint": dict(complaint)
        }

    finally:
        connection.close()


def update_complaint_status(
    complaint_id: str,
    new_status: str
):
    """
    Update the status of an existing complaint.
    """

    complaint_id = complaint_id.strip().upper()
    new_status = new_status.strip().title()

    if new_status not in VALID_STATUSES:
        raise ValueError("Invalid complaint status.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE complaints
            SET status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE complaint_id = ?
        """, (new_status, complaint_id))

        connection.commit()

        if cursor.rowcount == 0:
            return {
                "status": "not_found",
                "message": "No complaint found with this ID."
            }

        return {
            "status": "success",
            "complaint_id": complaint_id,
            "new_status": new_status,
            "message": "Complaint status updated successfully."
        }

    finally:
        connection.close()
