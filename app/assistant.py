"""A simple local policy assistant used for the first learning milestone.

This is deliberately deterministic: it retrieves the policy sentence with the
highest keyword overlap. It is NOT a real LLM and is not production-ready.
"""
from pathlib import Path
import re

POLICY_DIR = Path(__file__).resolve().parents[1] / "data" / "policies"


def _words(text: str) -> set[str]:
    """Convert text to lowercase tokens and normalize a few simple synonyms."""
    tokens = set(re.findall(r"[a-z0-9]+", text.lower()))
    if "one" in tokens and "time" in tokens and "password" in tokens:
        tokens.add("otp")
    if "unfamiliar" in tokens:
        tokens.add("unknown")
    # Tiny normalization rules help this demo match common question word forms.
    if "disputing" in tokens:
        tokens.add("dispute")
    if "disputed" in tokens:
        tokens.add("dispute")
    if "confirming" in tokens:
        tokens.add("confirm")
    if "transactions" in tokens:
        tokens.add("transaction")
    return tokens


def load_policy_documents() -> list[dict]:
    """Read each Markdown policy file and return its name and content."""
    documents = []
    for path in sorted(POLICY_DIR.glob("*.md")):
        documents.append({
            "source": path.name,
            "content": path.read_text(encoding="utf-8"),
        })
    return documents


def answer_question(question: str) -> dict:
    """Return a best-effort answer and source, or abstain if evidence is weak.

    Output shape:
        {"answer": str, "source": str | None, "abstained": bool}
    """
    question_words = _words(question)
    stop_words = {
        "what", "when", "where", "which", "does", "do", "is", "are", "can",
        "i", "my", "the", "a", "an", "to", "for", "of", "in", "on", "and",
        "or", "how", "please", "tell", "me", "about", "policy", "bank",
        "assistant", "should", "will", "would", "could", "if", "that",
        "i", "receive", "next", "year", "you", "guarantee", "tomorrow"
    }
    question_words -= stop_words

    best_sentence = ""
    best_source = None
    best_score = 0

    for document in load_policy_documents():
        # Remove Markdown headings so the first policy sentence is not discarded.
        body = "\n".join(line for line in document["content"].splitlines() if not line.strip().startswith("#"))
        sentences = re.split(r"(?<=[.!?])\s+", body.replace("\n", " "))
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence or sentence.startswith("#"):
                continue
            sentence_words = _words(sentence)
            score = len(question_words & sentence_words)
            # Small preference for a sentence that covers more of the question.
            if score > best_score:
                best_score = score
                best_sentence = sentence
                best_source = document["source"]

    if best_score < 2:
        return {
            "answer": "I don't have enough information in the available policy documents to answer that question.",
            "source": None,
            "abstained": True,
        }

    return {"answer": best_sentence, "source": best_source, "abstained": False}
