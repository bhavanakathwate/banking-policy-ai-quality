
import json
from pathlib import Path

from app.semantic_groundedness import check_semantic_groundedness


REPORT_PATH = Path("reports/semantic_evaluation_report.json")


def run_semantic_evaluation(cases: list[dict], evidence: str) -> dict:
    """Evaluate cases and report decision errors."""

    results = []

    for case in cases:
        actual = check_semantic_groundedness(
            answer=case["answer"],
            evidence=evidence,
        )

        expected = case["expected"]
        predicted = actual["passed"]

        false_accept = not expected and predicted
        false_reject = expected and not predicted
        matched = predicted == expected

        results.append({
            "name": case["name"],
            "expected": expected,
            "actual": predicted,
            "reason": actual["reason"],
            "test_passed": matched,
            "false_accept": false_accept,
            "false_reject": false_reject,
        })

    total = len(results)
    passed = sum(item["test_passed"] for item in results)
    false_accepts = sum(item["false_accept"] for item in results)
    false_rejects = sum(item["false_reject"] for item in results)

    report = {
        "evaluator": "Ollama semantic groundedness",
        "model": "qwen2.5:1.5b",
        "total_cases": total,
        "passed_cases": passed,
        "failed_cases": total - passed,
        "pass_rate": round(passed / total, 3) if total else 0,
        "false_accept_count": false_accepts,
        "false_reject_count": false_rejects,
        "results": results,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    return report
