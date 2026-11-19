
from database.complaint_repository import (
    register_complaint,
    get_complaint,
    update_complaint_status
)


# Test 1: Register complaint
result = register_complaint(
    category="Digital Banking",
    description=(
        "Unable to log in to the Ready Bank "
        "mobile application."
    )
)

print("\n--- Complaint Registration ---\n")
print(result)

# Save the generated ID for subsequent tests
complaint_id = result["complaint_id"]


# Test 2: Retrieve complaint
retrieved = get_complaint(complaint_id)

print("\n--- Complaint Details ---\n")
print(retrieved)


# Test 3: Update complaint status
updated = update_complaint_status(
    complaint_id,
    "In Progress"
)

print("\n--- Status Update ---\n")
print(updated)


# Test 4: Retrieve updated complaint
final_result = get_complaint(complaint_id)

print("\n--- Updated Complaint ---\n")
print(final_result)
