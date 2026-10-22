
from app.groundedness import check_groundedness


def evaluate_rag_result(result: dict) -> dict:
    """Evaluate a RAG response for citation and groundedness."""

    answer = result.get("answer", "")
    evidence = result.get("evidence", "")
    source = result.get("source")

    groundedness = check_groundedness(answer, evidence)

    citation_pass = bool(source and evidence.strip())

    passed = citation_pass and groundedness["passed"]

    return {
        "citation_pass": citation_pass,
        "groundedness_pass": groundedness["passed"],
        "groundedness_reason": groundedness["reason"],
        "passed": passed,
    }
