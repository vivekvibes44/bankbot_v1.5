
from tools.loan_tools import calculate_emi


def test_standard_emi():

    result = calculate_emi.invoke({
        "principal": 500000,
        "annual_interest_rate": 10,
        "tenure_months": 60
    })

    assert result["monthly_emi"] == 10623.52
    assert result["total_interest"] == 137411.34
    assert result["total_payment"] == 637411.34

    print("Standard EMI test passed.")


def test_zero_interest_emi():

    result = calculate_emi.invoke({
        "principal": 120000,
        "annual_interest_rate": 0,
        "tenure_months": 12
    })

    assert result["monthly_emi"] == 10000
    assert result["total_interest"] == 0
    assert result["total_payment"] == 120000

    print("Zero interest EMI test passed.")


def test_invalid_emi_inputs():

    invalid_cases = [
        {
            "principal": 0,
            "annual_interest_rate": 10,
            "tenure_months": 60
        },
        {
            "principal": -500000,
            "annual_interest_rate": 10,
            "tenure_months": 60
        },
        {
            "principal": 500000,
            "annual_interest_rate": -5,
            "tenure_months": 60
        },
        {
            "principal": 500000,
            "annual_interest_rate": 10,
            "tenure_months": 0
        },
        {
            "principal": 500000,
            "annual_interest_rate": 10,
            "tenure_months": -12
        }
    ]

    for case in invalid_cases:

        try:
            calculate_emi.invoke(case)

        except ValueError:
            continue

        raise AssertionError(
            f"Invalid EMI input was accepted: {case}"
        )

    print("All invalid EMI input tests passed.")


if __name__ == "__main__":

    test_standard_emi()
    test_zero_interest_emi()
    test_invalid_emi_inputs()

    print("\nAll EMI tests passed.")
