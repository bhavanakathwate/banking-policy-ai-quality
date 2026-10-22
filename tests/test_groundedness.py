
from app.groundedness import check_groundedness


def test_supported_answer_passes():
    result = check_groundedness(
        "Customers should never share their OTP",
        "Customers should never share their OTP, PIN, or password.",
    )

    assert result["passed"] is True


def test_unsupported_reimbursement_claim_fails():
    result = check_groundedness(
        "The bank guarantees reimbursement for every fraud loss.",
        "Customers should never share their OTP.",
    )

    assert result["passed"] is False


def test_empty_evidence_fails():
    result = check_groundedness("Never share your OTP.", "")

    assert result["passed"] is False


def test_empty_answer_fails():
    result = check_groundedness("", "Customers should never share their OTP.")

    assert result["passed"] is False


def test_correct_policy_plus_unsupported_promise_fails():
    evidence = (
        "Customers should never share their OTP, PIN, "
        "or password with anyone."
    )

    answer = (
        "Customers should never share their OTP, PIN, "
        "or password with anyone. "
        "The bank guarantees reimbursement for every fraud loss."
    )

    result = check_groundedness(answer, evidence)

    assert result["passed"] is False


def test_long_answer_with_unsupported_claim_fails():
    evidence = (
        "Customers should never share their one-time password "
        "(OTP), PIN, or password with anyone, including a bank employee. "
        "If a customer suspects unauthorized account access, they should "
        "immediately use the official banking app or the verified "
        "customer-support channel to secure the account. "
        "The bank will never ask a customer to disclose their full "
        "password or OTP over a phone call, email, or chat. "
        "Customers should review account activity regularly and report "
        "unfamiliar transactions through the official support channel."
    )

    answer = (
        evidence
        + " The bank guarantees reimbursement for every fraud loss."
    )

    result = check_groundedness(answer, evidence)

    assert result["passed"] is False


def test_valid_paraphrase_is_supported():
    evidence = (
        "Customers should never share their one-time password "
        "(OTP), PIN, or password with anyone, including a bank employee."
    )

    answer = (
        "Never disclose your OTP, PIN, or password to bank staff."
    )

    result = check_groundedness(answer, evidence)

    assert result["passed"] is True


def test_contradictory_answer_fails():
    evidence = (
        "Customers should never share their OTP, PIN, "
        "or password with anyone, including a bank employee."
    )

    answer = (
        "Customers can safely share their OTP with a bank employee."
    )

    result = check_groundedness(answer, evidence)

    assert result["passed"] is False
