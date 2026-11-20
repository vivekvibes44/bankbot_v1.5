
from tools.complaint_tools import (
    register_complaint,
    track_complaint
)


# Test 1: Attempt registration without confirmation
print("\n--- Registration Without Confirmation ---\n")

result = register_complaint.invoke({
    "category": "Digital Banking",
    "description": "Unable to log in to the mobile application.",
    "user_confirmation": False
})

print(result)


# Test 2: Register after confirmation
print("\n--- Registration With Confirmation ---\n")

result = register_complaint.invoke({
    "category": "Digital Banking",
    "description": "Unable to log in to the mobile application.",
    "user_confirmation": True
})

print(result)

# Store generated complaint ID
complaint_id = result["complaint_id"]


# Test 3: Track the registered complaint
print("\n--- Complaint Tracking ---\n")

tracking_result = track_complaint.invoke({
    "complaint_id": complaint_id
})

print(tracking_result)
