
from app.rag_evaluation import evaluate_rag_result


def test_supported_answer_with_source_passes():
    result = {
        "answer": "Customers should never share their OTP.",
        "source": "account_security.md",
        "evidence": (
            "Customers should never share their OTP, PIN, "
            "or password with anyone."
        ),
        "abstained": False,
    }

    evaluation = evaluate_rag_result(result)

    assert evaluation["citation_pass"] is True
    assert evaluation["groundedness_pass"] is True
    assert evaluation["passed"] is True


def test_unsupported_claim_fails_evaluation():
    result = {
        "answer": (
            "Never share your OTP. "
            "The bank guarantees reimbursement for every fraud loss."
        ),
        "source": "account_security.md",
        "evidence": "Customers should never share their OTP.",
        "abstained": False,
    }

    evaluation = evaluate_rag_result(result)

    assert evaluation["groundedness_pass"] is False
    assert evaluation["passed"] is False


def test_missing_source_fails_evaluation():
    result = {
        "answer": "Customers should never share their OTP.",
        "source": None,
        "evidence": "Customers should never share their OTP.",
        "abstained": False,
    }

    evaluation = evaluate_rag_result(result)

    assert evaluation["citation_pass"] is False
    assert evaluation["passed"] is False
