from langchain_core.tools import tool

from database.complaint_repository import (
    register_complaint as create_complaint_record,
    get_complaint
)


@tool
def register_complaint(
    category: str,
    description: str,
    user_confirmation: bool
):
    """
    Register a simulated Ready Bank complaint.

    Only call this tool after the user has explicitly
    confirmed that they want to submit the complaint.

    Args:
        category: Complaint category.
        description: Description of the complaint.
        user_confirmation: True only after explicit user confirmation.

    Returns:
        Complaint registration result with a unique complaint ID.
    """

    if user_confirmation is not True:
        return {
            "status": "confirmation_required",
            "message": (
                "The user must explicitly confirm complaint "
                "registration before submission."
            )
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

    if not complaint_id.strip():
        return {
            "status": "invalid_input",
            "message": "Complaint ID cannot be empty."
        }

    result = get_complaint(complaint_id)

    return result
