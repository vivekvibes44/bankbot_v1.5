
from tools.complaint_tools import (
    register_complaint,
    track_complaint
)


def test_invalid_category():
    result = register_complaint.invoke({
        "category": "Mobile Banking",
        "description": "Unable to access mobile banking."
    })

    assert result["status"] == "invalid_input"
    print("PASS: Invalid category")


def test_empty_description():
    result = register_complaint.invoke({
        "category": "Digital Banking",
        "description": ""
    })

    assert result["status"] == "invalid_input"
    print("PASS: Empty description")


def test_whitespace_description():
    result = register_complaint.invoke({
        "category": "Digital Banking",
        "description": "   "
    })

    assert result["status"] == "invalid_input"
    print("PASS: Whitespace-only description")


def test_empty_complaint_id():
    result = track_complaint.invoke({
        "complaint_id": ""
    })

    assert result["status"] == "invalid_input"
    print("PASS: Empty complaint ID")


def test_unknown_complaint_id():
    result = track_complaint.invoke({
        "complaint_id": "RB-UNKNOWN1"
    })

    assert result["status"] == "not_found"
    print("PASS: Unknown complaint ID")


if __name__ == "__main__":
    print("\n========== COMPLAINT TOOL EDGE CASE TESTS ==========\n")

    test_invalid_category()
    test_empty_description()
    test_whitespace_description()
    test_empty_complaint_id()
    test_unknown_complaint_id()

    print("\n========== ALL TESTS PASSED ==========\n")
