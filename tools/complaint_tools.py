from langchain_core.tools import tool
from langgraph.types import interrupt

from database.complaint_repository import (
    register_complaint as create_complaint_record,
    get_complaint,
    VALID_CATEGORIES
)


@tool
def register_complaint(category: str, description: str):
    """
    Register a simulated Ready Bank complaint.

    This tool pauses execution and requests explicit human
    approval before saving the complaint.

    Args:
        category: Complaint category.
        description: Description of the complaint.

    Returns:
        Complaint registration result.
    """

    category = category.strip()
    description = description.strip()

    # Validate before requesting approval.
    if category not in VALID_CATEGORIES:
        return {
            "status": "invalid_input",
            "message": (
                f"Invalid category. Choose one of: "
                f"{', '.join(VALID_CATEGORIES)}"
            )
        }

    if not description:
        return {
            "status": "invalid_input",
            "message": "Complaint description cannot be empty."
        }

    # Pause graph execution and wait for human approval.
    approval = interrupt({
        "type": "complaint_registration",
        "message": "Please review and confirm this complaint registration.",
        "category": category,
        "description": description
    })

    # Only an explicit approval allows database insertion.
    if not isinstance(approval, dict) or approval.get("approved") is not True:
        return {
            "status": "cancelled",
            "message": "Complaint registration was cancelled."
        }

    result = create_complaint_record(
        category=category,
        description=description
    )

    return result


@tool
def track_complaint(complaint_id: str):
    """
    Track an existing Ready Bank complaint.

    Args:
        complaint_id: Unique complaint ID provided during registration.

    Returns:
        Complaint details and current status.
    """

    complaint_id = complaint_id.strip()

    if not complaint_id:
        return {
            "status": "invalid_input",
            "message": "Complaint ID cannot be empty."
        }

    result = get_complaint(complaint_id)

    return result