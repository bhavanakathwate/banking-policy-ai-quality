
from unittest.mock import patch, Mock

import pytest

from app.semantic_groundedness import check_semantic_groundedness


def test_empty_evidence_fails_without_model_call():
    with patch(
        "app.semantic_groundedness.requests.post"
    ) as mock_post:
        result = check_semantic_groundedness(
            "Never share your OTP.",
            "",
        )

    assert result["passed"] is False
    mock_post.assert_not_called()


@pytest.mark.parametrize(
    ("answer", "model_decision", "expected"),
    [
        (
            "Never disclose your OTP, PIN, or password to bank staff.",
            "PASS",
            True,
        ),
        (
            "The bank guarantees reimbursement for every fraud loss.",
            "FAIL",
            False,
        ),
        (
            "Customers can safely share their OTP with a bank employee.",
            "FAIL",
            False,
        ),
    ],
)
def test_semantic_evaluation_uses_model_decision(
    answer, model_decision, expected
):
    mock_response = Mock()
    mock_response.json.return_value = {
        "response": model_decision
    }
    mock_response.raise_for_status.return_value = None

    with patch(
        "app.semantic_groundedness.requests.post",
        return_value=mock_response,
    ):
        result = check_semantic_groundedness(
            answer,
            "Customers should never share their OTP, PIN, or password.",
        )

    assert result["passed"] is expected


def test_unsupported_promise_without_guarantee_word_is_rejected():
    mock_response = Mock()
    mock_response.json.return_value = {"response": "PASS"}
    mock_response.raise_for_status.return_value = None

    evidence = (
        "Customers should report unfamiliar transactions "
        "through the official support channel."
    )
    answer = (
        "The bank will return all money lost to fraud."
    )

    with patch(
        "app.semantic_groundedness.requests.post",
        return_value=mock_response,
    ) as mock_post:
        result = check_semantic_groundedness(answer, evidence)

    assert result["passed"] is False


def test_compensation_is_allowed_when_evidence_supports_it():
    mock_response = Mock()
    mock_response.json.return_value = {"response": "PASS"}
    mock_response.raise_for_status.return_value = None

    evidence = (
        "Eligible customers may receive compensation for "
        "verified losses after a review."
    )
    answer = (
        "Eligible customers may receive compensation "
        "for verified losses after a review."
    )

    with patch(
        "app.semantic_groundedness.requests.post",
        return_value=mock_response,
    ):
        result = check_semantic_groundedness(answer, evidence)

    assert result["passed"] is True


def test_valid_paraphrase_without_promise_language_is_accepted():
    mock_response = Mock()
    mock_response.json.return_value = {"response": "PASS"}
    mock_response.raise_for_status.return_value = None

    evidence = (
        "Customers should regularly review account activity."
    )
    answer = (
        "Customers should check their account activity regularly."
    )

    with patch(
        "app.semantic_groundedness.requests.post",
        return_value=mock_response,
    ):
        result = check_semantic_groundedness(answer, evidence)

    assert result["passed"] is True


def test_supported_compensation_claim_is_accepted():
    evidence = (
        "Eligible customers may receive compensation for "
        "verified losses after a review."
    )
    answer = (
        "Eligible customers may receive compensation for "
        "verified losses after a review."
    )

    mock_response = Mock()
    mock_response.json.return_value = {"response": "PASS"}
    mock_response.raise_for_status.return_value = None

    with patch(
        "app.semantic_groundedness.requests.post",
        return_value=mock_response,
    ) as mock_post:
        result = check_semantic_groundedness(answer, evidence)

    assert result["passed"] is True
    mock_post.assert_called_once()


def test_unsupported_refund_promise_with_different_wording_is_rejected():
    evidence = (
        "Customers should report unfamiliar transactions "
        "through the official support channel."
    )
    answer = (
        "Every customer will get all stolen money back."
    )

    mock_response = Mock()
    mock_response.json.return_value = {"response": "PASS"}
    mock_response.raise_for_status.return_value = None

    with patch(
        "app.semantic_groundedness.requests.post",
        return_value=mock_response,
    ):
        result = check_semantic_groundedness(answer, evidence)

    assert result["passed"] is False


def test_supported_paraphrase_is_accepted_with_mocked_model():
    evidence = (
        "Customers should regularly review account activity."
    )
    answer = (
        "Customers should check their account activity regularly."
    )

    mock_response = Mock()
    mock_response.json.return_value = {"response": "PASS"}
    mock_response.raise_for_status.return_value = None

    with patch(
        "app.semantic_groundedness.requests.post",
        return_value=mock_response,
    ):
        result = check_semantic_groundedness(answer, evidence)

    assert result["passed"] is True
