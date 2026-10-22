
import math

import pytest

import app.embedding_retriever as retriever


def test_empty_question_raises_error():
    with pytest.raises(ValueError, match="must not be empty"):
        retriever.retrieve_policy_embedding("   ")


def test_no_documents_returns_empty_result(monkeypatch):
    monkeypatch.setattr(retriever, "load_policy_documents", lambda: [])

    result = retriever.retrieve_policy_embedding("How do I secure my account?")

    assert result == {
        "source": None,
        "evidence": "",
        "score": 0,
    }


def test_retrieves_most_similar_policy(monkeypatch):
    documents = [
        {"source": "account_security.md", "content": "Account security policy"},
        {"source": "card_disputes.md", "content": "Card dispute policy"},
    ]
    monkeypatch.setattr(
        retriever, "load_policy_documents", lambda: documents
    )

    # First vector is for the question; next two are for the documents.
    embeddings = iter([
        [1.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
    ])
    monkeypatch.setattr(
        retriever, "_get_embedding", lambda text: next(embeddings)
    )

    result = retriever.retrieve_policy_embedding("How do I secure my account?")

    assert result["source"] == "account_security.md"
    assert result["evidence"] == "Account security policy"
    assert result["score"] == pytest.approx(1.0)


def test_abstains_when_similarity_is_below_threshold(monkeypatch):
    documents = [
        {"source": "digital_transfers.md", "content": "Digital transfers policy"},
    ]
    monkeypatch.setattr(
        retriever, "load_policy_documents", lambda: documents
    )

    embeddings = iter([
        [1.0, 0.0],
        [0.3, math.sqrt(0.91)],
    ])
    monkeypatch.setattr(
        retriever, "_get_embedding", lambda text: next(embeddings)
    )

    result = retriever.retrieve_policy_embedding("What is the weather on Mars?")

    assert result["source"] is None
    assert result["evidence"] == ""
    assert result["score"] == pytest.approx(0.3)


def test_cosine_similarity_handles_zero_vector():
    assert retriever._cosine_similarity([0.0, 0.0], [1.0, 0.0]) == 0.0


def test_cosine_similarity_rejects_different_dimensions():
    with pytest.raises(ValueError, match="same dimensions"):
        retriever._cosine_similarity([1.0, 0.0], [1.0])
