
import re


IGNORED_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "should", "must", "to", "of", "and", "or", "with",
    "their", "your", "they", "it", "be", "can", "anyone",
    "customers", "customer", "including",
}

EQUIVALENT_PHRASES = {
    "one-time password": "otp",
    "disclose": "share",
    "bank staff": "bank employee",
    "bank employees": "bank employee",
    "using": "use",
}


def normalize_text(text: str) -> str:
    """Normalize text and a small set of known equivalent phrases."""
    text = text.lower()

    for phrase, replacement in EQUIVALENT_PHRASES.items():
        text = text.replace(phrase, replacement)

    return re.sub(r"[^\w\s]", " ", text).strip()


def meaningful_words(text: str) -> set[str]:
    """Return unique words after normalization and stop-word removal."""
    normalized = normalize_text(text)

    return {
        word
        for word in normalized.split()
        if word not in IGNORED_WORDS
    }


def check_groundedness(answer: str, evidence: str) -> dict:
    """Check whether each answer sentence matches policy evidence."""

    if not answer.strip() or not evidence.strip():
        return {
            "passed": False,
            "reason": "Answer or evidence is empty.",
        }

    answer_sentences = [
        sentence.strip()
        for sentence in re.split(r"[.!?]+", answer)
        if sentence.strip()
    ]

    evidence_sentences = [
        sentence.strip()
        for sentence in re.split(r"[.!?]+", evidence)
        if sentence.strip()
    ]

    evidence_word_sets = [
        meaningful_words(sentence)
        for sentence in evidence_sentences
    ]

    unsupported_sentences = []

    for sentence in answer_sentences:
        answer_words = meaningful_words(sentence)

        if not answer_words:
            unsupported_sentences.append(sentence)
            continue

        supported = any(
            answer_words.issubset(evidence_words)
            for evidence_words in evidence_word_sets
        )

        if not supported:
            unsupported_sentences.append(sentence)

    if unsupported_sentences:
        return {
            "passed": False,
            "reason": (
                "Potentially unsupported sentence(s): "
                + " | ".join(unsupported_sentences)
            ),
        }

    return {
        "passed": True,
        "reason": "All answer sentences match the evidence after normalization.",
    }
