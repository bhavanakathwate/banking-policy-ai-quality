
from sklearn.feature_extraction.text import TfidfVectorizer

from app.assistant import load_policy_documents


def retrieve_policy(question: str) -> dict:
    """Find the most relevant policy document using TF-IDF similarity."""

    if not question.strip():
        raise ValueError("Question must not be empty.")

    documents = load_policy_documents()

    if not documents:
        return {
            "source": None,
            "evidence": "",
            "score": 0,
        }

    contents = [document["content"] for document in documents]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
    )

    try:
        document_vectors = vectorizer.fit_transform(contents)
        question_vector = vectorizer.transform([question])
    except ValueError:
        # Handles documents containing no usable vocabulary.
        return {
            "source": None,
            "evidence": "",
            "score": 0,
        }

    similarities = (
        document_vectors @ question_vector.T
    ).toarray().flatten()

    best_index = similarities.argmax()
    best_score = float(similarities[best_index])

    if best_score <= 0:
        return {
            "source": None,
            "evidence": "",
            "score": 0,
        }

    return {
        "source": documents[best_index]["source"],
        "evidence": documents[best_index]["content"],
        "score": best_score,
    }
