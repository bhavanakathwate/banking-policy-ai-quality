
import json
from pathlib import Path

from app.retriever import retrieve_policy


REPORT_PATH = Path("reports/retrieval_benchmark_report.json")

TEST_CASES = [
    {
        "name": "Unauthorized account access",
        "question": "What should I do if someone accessed my account without permission?",
        "expected_source": "account_security.md",
    },
    {
        "name": "OTP sharing",
        "question": "Should I tell a bank employee my OTP?",
        "expected_source": "account_security.md",
    },
    {
        "name": "Unfamiliar transaction",
        "question": "How do I report a transaction I don't recognize?",
        "expected_source": "card_disputes.md",
    },
    {
        "name": "Account security guidance",
        "question": "How can I secure my account if I suspect unauthorized access?",
        "expected_source": "account_security.md",
    },
    {
        "name": "Unrelated weather question",
        "question": "What is the weather on Mars?",
        "expected_source": None,
    },
]


def run_retrieval_benchmark() -> dict:
    results = []

    for case in TEST_CASES:
        actual = retrieve_policy(case["question"])
        expected_source = case["expected_source"]
        actual_source = actual["source"]

        matched = actual_source == expected_source

        results.append({
            "name": case["name"],
            "question": case["question"],
            "expected_source": expected_source,
            "actual_source": actual_source,
            "score": actual["score"],
            "matched": matched,
        })

    total = len(results)
    matched_count = sum(item["matched"] for item in results)

    report = {
        "retriever": "TF-IDF",
        "total_cases": total,
        "matched_cases": matched_count,
        "failed_cases": total - matched_count,
        "accuracy": round(matched_count / total, 3) if total else 0,
        "results": results,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    return report


if __name__ == "__main__":
    report = run_retrieval_benchmark()

    print("Retrieval benchmark report")
    print(f"Total cases: {report['total_cases']}")
    print(f"Matched cases: {report['matched_cases']}")
    print(f"Failed cases: {report['failed_cases']}")
    print(f"Accuracy: {report['accuracy']:.0%}")
    print(f"Report: {REPORT_PATH}")

    for result in report["results"]:
        status = "PASS" if result["matched"] else "FAIL"
        print(
            f"[{status}] {result['name']} | "
            f"expected={result['expected_source']} | "
            f"actual={result['actual_source']} | "
            f"score={result['score']}"
        )
