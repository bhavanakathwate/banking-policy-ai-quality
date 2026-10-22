
import json
from pathlib import Path

from app.embedding_retriever import retrieve_policy_embedding


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = PROJECT_ROOT / "reports" / "embedding_retrieval_benchmark_report.json"


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

    {
        "name": "Paraphrased account compromise",
        "question": "I think a stranger got into my bank account. How can I protect it?",
        "expected_source": "account_security.md",
    },
    {
        "name": "Transaction dispute required details",
        "question": "What information should I provide when challenging a card payment?",
        "expected_source": "card_disputes.md",
    },
    {
        "name": "Sensitive information safety",
        "question": "Is it safe to send my PIN or password in a chat message?",
        "expected_source": "card_disputes.md",
    },
    {
        "name": "Unrelated cooking question",
        "question": "How long should I bake a chocolate cake?",
        "expected_source": None,
    },
   {
        "name": "Refund guarantee policy",
        "question": "Can you guarantee that I will get my money back tomorrow?",
        "expected_source": "card_disputes.md",
    },

]


def run_benchmark() -> dict:
    results = []

    for case in TEST_CASES:
        retrieval = retrieve_policy_embedding(case["question"])
        actual_source = retrieval["source"]
        expected_source = case["expected_source"]

        results.append({
            **case,
            "actual_source": actual_source,
            "score": round(retrieval["score"], 4),
            "matched": actual_source == expected_source,
        })

    total_cases = len(results)
    matched_cases = sum(result["matched"] for result in results)

    report = {
        "retriever": "Ollama embeddings (nomic-embed-text)",
        "total_cases": total_cases,
        "matched_cases": matched_cases,
        "failed_cases": total_cases - matched_cases,
        "accuracy": matched_cases / total_cases if total_cases else 0,
        "results": results,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    return report


if __name__ == "__main__":
    report = run_benchmark()

    print("Embedding retrieval benchmark")
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
