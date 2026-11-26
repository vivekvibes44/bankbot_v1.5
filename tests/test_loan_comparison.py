from tools.loan_tools import compare_loans, LOAN_CRITERIA


def test_loan_comparison():

    print("\n--- Loan Comparison Verification ---")

    result = compare_loans.invoke({})

    # Verify successful response.
    assert result["status"] == "success"

    loans = result["available_loans"]

    # Verify all configured loans are returned.
    assert len(loans) == len(LOAN_CRITERIA)

    expected_loan_types = [
        "Home Loan",
        "Education Loan",
        "Personal Loan"
    ]

    actual_loan_types = [
        loan["loan_type"]
        for loan in loans
    ]

    assert actual_loan_types == expected_loan_types

    print("Loan product retrieval test passed.")

    # Verify ascending interest rate order.
    interest_rates = [
        loan["annual_interest_rate"]
        for loan in loans
    ]

    assert interest_rates == sorted(interest_rates)

    print("Interest rate sorting test passed.")

    # Verify required fields.
    required_fields = [
        "loan_type",
        "minimum_age",
        "maximum_age",
        "minimum_monthly_income",
        "annual_interest_rate",
        "maximum_tenure_years"
    ]

    for loan in loans:

        for field in required_fields:
            assert field in loan, (
                f"Missing field {field} in {loan['loan_type']}"
            )

    print("Required fields test passed.")

    # Verify comparison data against LOAN_CRITERIA.
    for loan in loans:

        criteria = LOAN_CRITERIA[loan["loan_type"].lower()]

        assert loan["minimum_age"] == criteria["minimum_age"]
        assert loan["maximum_age"] == criteria["maximum_age"]

        assert (
            loan["minimum_monthly_income"]
            == criteria["minimum_income"]
        )

        assert (
            loan["annual_interest_rate"]
            == criteria["interest_rate"]
        )

        assert (
            loan["maximum_tenure_years"]
            == criteria["maximum_tenure_years"]
        )

    print("Loan criteria consistency test passed.")

    # Verify comparison basis and disclaimer.
    assert result["comparison_basis"] == (
        "Annual interest rate, lowest first"
    )

    assert result["disclaimer"].strip()

    print("Comparison basis and disclaimer tests passed.")

    print("\nVerified loan comparison:")

    for loan in loans:
        print(
            f"{loan['loan_type']}: "
            f"{loan['annual_interest_rate']}%"
        )


if __name__ == "__main__":

    test_loan_comparison()

    print("\nAll loan comparison tests passed.")
