from tools.loan_tools import check_loan_eligibility


def test_eligible_applicants():

    cases = [
        {
            "loan_type": "personal loan",
            "age": 30,
            "monthly_income": 50000
        },
        {
            "loan_type": "home loan",
            "age": 35,
            "monthly_income": 80000
        },
        {
            "loan_type": "education loan",
            "age": 25,
            "monthly_income": 30000
        }
    ]

    for case in cases:

        result = check_loan_eligibility.invoke(case)

        assert result["status"] == "eligible", result
        assert result["preliminary_eligibility"] is True

    print("All eligible applicant tests passed.")


def test_ineligible_applicants():

    cases = [
        {
            "loan_type": "personal loan",
            "age": 19,
            "monthly_income": 20000
        },
        {
            "loan_type": "home loan",
            "age": 30,
            "monthly_income": 30000
        },
        {
            "loan_type": "education loan",
            "age": 40,
            "monthly_income": 20000
        }
    ]

    for case in cases:

        result = check_loan_eligibility.invoke(case)

        assert result["status"] == "not_eligible", result
        assert result["preliminary_eligibility"] is False
        assert len(result["reasons"]) > 0

    print("All ineligible applicant tests passed.")


def test_eligibility_boundaries():

    cases = [
        # Personal loan: minimum age and income
        {
            "loan_type": "personal loan",
            "age": 21,
            "monthly_income": 25000
        },
        # Personal loan: maximum age
        {
            "loan_type": "personal loan",
            "age": 60,
            "monthly_income": 25000
        },
        # Home loan: maximum age
        {
            "loan_type": "home loan",
            "age": 65,
            "monthly_income": 40000
        },
        # Education loan: minimum age and income
        {
            "loan_type": "education loan",
            "age": 18,
            "monthly_income": 15000
        },
        # Education loan: maximum age
        {
            "loan_type": "education loan",
            "age": 35,
            "monthly_income": 15000
        }
    ]

    for case in cases:

        result = check_loan_eligibility.invoke(case)

        assert result["status"] == "eligible", result

    print("All eligibility boundary tests passed.")


def test_invalid_loan_type():

    result = check_loan_eligibility.invoke({
        "loan_type": "vehicle loan",
        "age": 30,
        "monthly_income": 50000
    })

    assert result["status"] == "invalid_loan_type"

    print("Invalid loan type test passed.")


def test_invalid_inputs():

    cases = [
        {
            "loan_type": "personal loan",
            "age": 0,
            "monthly_income": 50000
        },
        {
            "loan_type": "personal loan",
            "age": -5,
            "monthly_income": 50000
        },
        {
            "loan_type": "personal loan",
            "age": 30,
            "monthly_income": -1000
        }
    ]

    for case in cases:

        result = check_loan_eligibility.invoke(case)

        assert result["status"] == "invalid_input", result

    print("All invalid input tests passed.")


if __name__ == "__main__":

    test_eligible_applicants()
    test_ineligible_applicants()
    test_eligibility_boundaries()
    test_invalid_loan_type()
    test_invalid_inputs()

    print("\nAll loan eligibility tests passed.")
