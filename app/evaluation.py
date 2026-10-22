"""Evaluation helpers for the Banking Policy Assistant starter project."""
from pathlib import Path
import json
from app.assistant import answer_question, load_policy_documents
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TEST_CASES_PATH = ROOT / "data" / "test_cases.json"

def normalize_text(text: str) -> str:
    """Make simple text comparisons consistent."""
    return " ".join(text.lower().split())

def is_grounded(answer: str, evidence: str) -> bool:
    """Check whether the answer is supported by the supplied evidence."""
    #return True  # TEMPORARY MUTATION â€” remove immediately
    answer_text = normalize_text(answer)
    evidence_text = normalize_text(evidence)

    if not answer_text or not evidence_text:
        return False

    if answer_text in evidence_text:
        return True

    equivalent_phrases = {
        "do not disclose": "never share",
        "bank staff": "bank employee",
        "to bank employee": "with a bank employee",
    }

    for phrase, equivalent in equivalent_phrases.items():
        answer_text = answer_text.replace(phrase, equivalent)

    ignored_words = {"a", "customers", "should", "their", "your"}
    answer_text = " ".join(
        word for word in answer_text.split() if word not in ignored_words
    )
    evidence_text = " ".join(
        word for word in evidence_text.split() if word not in ignored_words
    )

    return answer_text in evidence_text

def load_test_cases() -> list[dict]:
    """Load test cases from JSON."""
    return json.loads(TEST_CASES_PATH.read_text(encoding="utf-8"))


def evaluate_case(test_case: dict) -> dict:
    """Run one test case and calculate simple, explainable checks."""
    result = answer_question(test_case["question"])
    source_documents = {
        document["source"]: document["content"]
        for document in load_policy_documents()
    }

    evidence = source_documents.get(result["source"], "")
    if result["abstained"]:
        groundedness_pass = True
    else:
        groundedness_pass = is_grounded(result["answer"], evidence)

    expected_answerable = test_case["answerable"]
    answerability_pass = result["abstained"] == (not expected_answerable)

    required_terms = [term.lower() for term in test_case.get("required_terms", [])]
    answer_lower = " ".join(result["answer"].lower().split())
    matched_terms = [term for term in required_terms if term in answer_lower]
    term_coverage = len(matched_terms) / len(required_terms) if required_terms else 1.0

    citation_pass = (
    (not expected_answerable and result["source"] is None)
    or (
        expected_answerable
        and result["source"] in source_documents
        )
    )
    case_pass = (
        answerability_pass
        and term_coverage >= 0.80
        and citation_pass
        and groundedness_pass
    )

    return {
        "id": test_case["id"],
        "severity": test_case.get("severity", "medium"),
        "question": test_case["question"],
        "expected_answerable": expected_answerable,
        "actual_abstained": result["abstained"],
        "abstained": result["abstained"],
        "answer": result["answer"],
        "source": result["source"],
        "required_terms": required_terms,
        "matched_terms": matched_terms,
        "term_coverage": round(term_coverage, 2),
        "answerability_pass": answerability_pass,
        "citation_pass": citation_pass,
        "groundedness_pass": groundedness_pass,
        "passed": case_pass,
        "evidence": evidence,

    }


def build_report() -> dict:
    """Evaluate all cases and return summary metrics plus case details."""
    evaluated = [evaluate_case(case) for case in load_test_cases()]

    total = len(evaluated)
    passed = sum(case["passed"] for case in evaluated)
    answerability_passed = sum(case["answerability_pass"] for case in evaluated)
    citation_passed = sum(case["citation_pass"] for case in evaluated)

    critical_failures = [
        case
        for case in evaluated
        if case["severity"] == "critical" and not case["passed"]
    ]

    release_pass = len(critical_failures) == 0

    failed_cases = [case for case in evaluated if not case["passed"]]

    failure_summary = {
        "total_failures": len(failed_cases),
        "critical": sum(
            1 for case in failed_cases if case["severity"] == "critical"
        ),
        "high": sum(
            1 for case in failed_cases if case["severity"] == "high"
        ),
        "medium": sum(
            1 for case in failed_cases if case["severity"] == "medium"
        ),
        "low": sum(
            1 for case in failed_cases if case["severity"] == "low"
        ),
        "failed_case_ids": [case["id"] for case in failed_cases],
    }

    unanswerable_cases = [case for case in evaluated if not case["expected_answerable"]]
    unsupported_answers = sum(
        1 for case in unanswerable_cases if not case["actual_abstained"]
    )

    return {
        "project": "Banking Policy Assistant AI Quality Evaluation Framework",
        "note": "Starter deterministic retrieval baseline; not a real LLM evaluation.",
        "metrics": {
            "total_cases": total,
            "passed_cases": passed,
            "overall_pass_rate": round(passed / total, 3) if total else 0,
            "answerability_accuracy": round(answerability_passed / total, 3) if total else 0,
            "citation_check_rate": round(citation_passed / total, 3) if total else 0,
            "groundedness_pass_rate": round(
                sum(case["groundedness_pass"] for case in evaluated) / total, 3
            ) if total else 0,
            "unsupported_answer_rate": round(
                unsupported_answers / len(unanswerable_cases), 3
            ) if unanswerable_cases else 0,
            "required_term_coverage_average": round(
                sum(case["term_coverage"] for case in evaluated) / total, 3
            ) if total else 0,
        },
        "cases": evaluated,
        "critical_failure_count": len(critical_failures),
        "failure_summary": failure_summary,
        "release_pass": release_pass,
    }
