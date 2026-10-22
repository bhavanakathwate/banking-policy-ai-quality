
import math
import re

import requests

from app.assistant import load_policy_documents


OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "nomic-embed-text"
SIMILARITY_THRESHOLD = 0.50
_paragraph_embedding_cache: dict[str, list[float]] = {}

def _get_embedding(text: str) -> list[float]:
    """Convert text into a numerical embedding using Ollama."""

    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": EMBEDDING_MODEL,
            "input": text,
        },
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    embeddings = data["embeddings"]

    if not embeddings or not embeddings[0]:
        raise ValueError("The embedding model returned an empty embedding.")

    return embeddings[0]

def _get_cached_embedding(text: str) -> list[float]:
    """Reuse an embedding if this text has already been processed."""

    if text not in _paragraph_embedding_cache:
        _paragraph_embedding_cache[text] = _get_embedding(text)

    return _paragraph_embedding_cache[text]


def _cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """Calculate cosine similarity between two embedding vectors."""

    if len(vector_a) != len(vector_b):
        raise ValueError("Embedding vectors must have the same dimensions.")

    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    norm_a = math.sqrt(sum(value * value for value in vector_a))
    norm_b = math.sqrt(sum(value * value for value in vector_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def _split_into_paragraphs(content: str) -> list[str]:
    """Split a Markdown policy into non-empty paragraphs."""

    paragraphs = re.split(r"\n\s*\n", content.strip())

    return [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip() and not paragraph.strip().startswith("#")
    ]


def retrieve_policy_embedding(question: str) -> dict:
    """Retrieve the most relevant policy paragraph using embeddings."""

    if not question.strip():
        raise ValueError("Question must not be empty.")

    documents = load_policy_documents()

    if not documents:
        return {
            "source": None,
            "evidence": "",
            "score": 0,
        }

    question_embedding = _get_embedding(question)

    best_source = None
    best_paragraph = ""
    best_score = -1.0

    for document in documents:
        paragraphs = _split_into_paragraphs(document["content"])

        for paragraph in paragraphs:
            paragraph_embedding = _get_cached_embedding(paragraph)

            score = _cosine_similarity(
                question_embedding,
                paragraph_embedding,
            )

            if score > best_score:
                best_score = score
                best_source = document["source"]
                best_paragraph = paragraph

    if best_source is None or best_score < SIMILARITY_THRESHOLD:
        return {
            "source": None,
            "evidence": "",
            "score": max(best_score, 0.0),
        }

    return {
        "source": best_source,
        "evidence": best_paragraph,
        "score": best_score,
    }
