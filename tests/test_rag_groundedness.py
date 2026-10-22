
from unittest.mock import patch

from app.rag_assistant import answer_with_rag


@patch("app.rag_assistant.generate_answer")
@patch("app.rag_assistant.retrieve_policy")
def test_rag_returns_the_evidence_used(
    mock_retrieve, mock_generate
):
    evidence = (
        "Customers should never share their OTP, PIN, "
        "or password with anyone, including a bank employee."
    )

    mock_retrieve.return_value = {
        "source": "account_security.md",
        "evidence": evidence,
        "score": 5,
    }
    mock_generate.return_value = "Never share your OTP."

    result = answer_with_rag("Can I share my OTP?")

    assert result["evidence"] == evidence
    assert result["source"] == "account_security.md"


@patch("app.rag_assistant.generate_answer")
@patch("app.rag_assistant.retrieve_policy")
def test_rag_does_not_hide_unsupported_model_claim(
    mock_retrieve, mock_generate
):
    evidence = "Customers should never share their OTP."

    mock_retrieve.return_value = {
        "source": "account_security.md",
        "evidence": evidence,
        "score": 3,
    }
    mock_generate.return_value = (
        "Never share your OTP. "
        "The bank guarantees reimbursement for every fraud loss."
    )

    result = answer_with_rag("Can I share my OTP?")

    assert "guarantees reimbursement" in result["answer"]
    assert evidence == result["evidence"]
