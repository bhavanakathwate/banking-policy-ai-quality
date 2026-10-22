
from unittest.mock import Mock, patch

import pytest

from app.local_llm_adapter import generate_answer


def test_empty_question_raises_error():
    with pytest.raises(ValueError):
        generate_answer("", "Customers must never share their OTP.")


def test_empty_evidence_abstains_without_calling_ollama():
    with patch("app.local_llm_adapter.requests.post") as mock_post:
        answer = generate_answer("Can I share my OTP?", "")

    assert "cannot answer" in answer.lower()
    mock_post.assert_not_called()


@patch("app.local_llm_adapter.requests.post")
def test_successful_response_returns_model_answer(mock_post):
    mock_response = Mock()
    mock_response.json.return_value = {
        "response": "Never share your OTP with anyone."
    }
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    answer = generate_answer(
        "Can I share my OTP?",
        "Customers must never share their OTP.",
    )

    assert answer == "Never share your OTP with anyone."
    mock_post.assert_called_once()

    request_body = mock_post.call_args.kwargs["json"]
    assert request_body["model"] == "qwen2.5:1.5b"
    assert request_body["stream"] is False
    assert "Customers must never share their OTP." in request_body["prompt"]


@patch("app.local_llm_adapter.requests.post")
def test_http_error_is_propagated(mock_post):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = (
        __import__("requests").exceptions.HTTPError("Server error")
    )
    mock_post.return_value = mock_response

    with pytest.raises(__import__("requests").exceptions.HTTPError):
        generate_answer(
            "Can I share my OTP?",
            "Customers must never share their OTP.",
        )
