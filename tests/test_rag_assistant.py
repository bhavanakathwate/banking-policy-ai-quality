
from unittest.mock import patch

from app.rag_assistant import answer_with_rag


@patch("app.rag_assistant.generate_answer")
@patch("app.rag_assistant.retrieve_policy")
def test_rag_uses_retrieved_evidence(mock_retrieve, mock_generate):
    mock_retrieve.return_value = {
        "source": "account_security.md",
        "evidence": "Customers must never share their OTP.",
        "score": 3,
    }
    mock_generate.return_value = "Never share your OTP."

    result = answer_with_rag("Can I share my OTP?")

    assert result["answer"] == "Never share your OTP."
    assert result["source"] == "account_security.md"
    assert result["abstained"] is False

    mock_generate.assert_called_once_with(
        question="Can I share my OTP?",
        evidence="Customers must never share their OTP.",
    )


@patch("app.rag_assistant.generate_answer")
@patch("app.rag_assistant.retrieve_policy")
def test_rag_abstains_when_no_evidence(mock_retrieve, mock_generate):
    mock_retrieve.return_value = {
        "source": None,
        "evidence": "",
        "score": 0,
    }

    result = answer_with_rag("What is my mortgage rate?")

    assert result["abstained"] is True
    assert result["source"] is None
    mock_generate.assert_not_called()
