
from unittest.mock import patch

import pytest

from app.retriever import retrieve_policy


def test_empty_question_raises_error():
    with pytest.raises(ValueError):
        retrieve_policy("")


@patch("app.retriever.load_policy_documents")
def test_retrieves_document_with_matching_terms(mock_load):
    mock_load.return_value = [
        {
            "source": "account_security.md",
            "content": "Never share your OTP or PIN with anyone.",
        },
        {
            "source": "card_disputes.md",
            "content": "Report unauthorized card transactions promptly.",
        },
    ]

    result = retrieve_policy("Should I share my OTP?")

    assert result["source"] == "account_security.md"
    assert result["evidence"] == (
        "Never share your OTP or PIN with anyone."
    )
    assert result["score"] > 0


@patch("app.retriever.load_policy_documents")
def test_returns_empty_evidence_when_no_terms_match(mock_load):
    mock_load.return_value = [
        {
            "source": "card_disputes.md",
            "content": "Report unauthorized card transactions promptly.",
        }
    ]

    result = retrieve_policy("Tell me about my mortgage")

    assert result["source"] is None
    assert result["evidence"] == ""
    assert result["score"] == 0


@patch("app.retriever.load_policy_documents")
def test_retrieves_account_security_for_unauthorized_access_question(
    mock_load,
):
    mock_load.return_value = [
        {
            "source": "account_security.md",
            "content": (
                "If a customer suspects unauthorized account access, "
                "they should use the official banking app or verified "
                "customer support to secure the account."
            ),
        },
        {
            "source": "card_disputes.md",
            "content": (
                "Customers should report unfamiliar card transactions "
                "through the official support channel."
            ),
        },
    ]

    result = retrieve_policy(
        "What should I do if someone accessed my account without permission?"
    )

    assert result["source"] == "account_security.md"
    assert result["score"] > 0


@patch("app.retriever.load_policy_documents")
def test_retrieves_policy_for_otp_question(mock_load):
    mock_load.return_value = [
        {
            "source": "account_security.md",
            "content": (
                "Customers should never share their OTP, PIN, "
                "or password with a bank employee."
            ),
        },
        {
            "source": "card_disputes.md",
            "content": (
                "Report unfamiliar card transactions through "
                "official support."
            ),
        },
    ]

    result = retrieve_policy("Should I tell a bank employee my OTP?")

    assert result["source"] == "account_security.md"
    assert result["score"] > 0


@patch("app.retriever.load_policy_documents")
def test_retrieves_transaction_reporting_policy(mock_load):
    mock_load.return_value = [
        {
            "source": "account_security.md",
            "content": (
                "Customers should review account activity regularly "
                "and report unfamiliar transactions through official support."
            ),
        },
        {
            "source": "loan_policy.md",
            "content": (
                "Loan repayments must be made according to "
                "the agreed repayment schedule."
            ),
        },
    ]

    result = retrieve_policy(
        "How do I report a transaction I don't recognize?"
    )

    assert result["source"] == "account_security.md"
    assert result["score"] > 0


@patch("app.retriever.load_policy_documents")
def test_returns_no_source_for_unrelated_question(mock_load):
    mock_load.return_value = [
        {
            "source": "account_security.md",
            "content": (
                "Customers should never share OTPs or passwords."
            ),
        },
        {
            "source": "card_disputes.md",
            "content": (
                "Report unfamiliar card transactions through support."
            ),
        },
    ]

    result = retrieve_policy("What is the weather on Mars?")

    assert result["source"] is None
    assert result["evidence"] == ""
    assert result["score"] == 0


@patch("app.retriever.load_policy_documents")
def test_retrieves_security_policy_for_security_question(mock_load):
    mock_load.return_value = [
        {
            "source": "account_security.md",
            "content": (
                "If a customer suspects unauthorized account access, "
                "they should immediately use the official banking app "
                "or verified customer support to secure the account."
            ),
        },
        {
            "source": "card_disputes.md",
            "content": (
                "Customers should report unfamiliar card transactions "
                "through official support."
            ),
        },
    ]

    result = retrieve_policy(
        "How can I secure my account if I suspect unauthorized access?"
    )

    assert result["source"] == "account_security.md"
    assert result["score"] > 0
