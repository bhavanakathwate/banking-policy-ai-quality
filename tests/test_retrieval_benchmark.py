
import json
from unittest.mock import patch

from app import run_retrieval_benchmark as benchmark


def test_retrieval_benchmark_all_cases_match():
    with patch.object(
        benchmark,
        "retrieve_policy",
    ) as mock_retrieve:
        mock_retrieve.side_effect = [
            {"source": "account_security.md", "evidence": "evidence", "score": 0.4},
            {"source": "account_security.md", "evidence": "evidence", "score": 0.3},
            {"source": "card_disputes.md", "evidence": "evidence", "score": 0.3},
            {"source": "account_security.md", "evidence": "evidence", "score": 0.4},
            {"source": None, "evidence": "", "score": 0},
        ]

        report = benchmark.run_retrieval_benchmark()

    assert report["total_cases"] == 5
    assert report["matched_cases"] == 5
    assert report["failed_cases"] == 0
    assert report["accuracy"] == 1.0


def test_retrieval_benchmark_writes_json_report(tmp_path):
    report_path = tmp_path / "retrieval_benchmark_report.json"

    with (
        patch.object(benchmark, "REPORT_PATH", report_path),
        patch.object(
            benchmark,
            "retrieve_policy",
        ) as mock_retrieve,
    ):
        mock_retrieve.side_effect = [
            {"source": "account_security.md", "evidence": "evidence", "score": 0.4},
            {"source": "account_security.md", "evidence": "evidence", "score": 0.3},
            {"source": "card_disputes.md", "evidence": "evidence", "score": 0.3},
            {"source": "account_security.md", "evidence": "evidence", "score": 0.4},
            {"source": None, "evidence": "", "score": 0},
        ]

        benchmark.run_retrieval_benchmark()

    assert report_path.exists()

    saved_report = json.loads(
        report_path.read_text(encoding="utf-8")
    )

    assert saved_report["total_cases"] == 5
    assert saved_report["matched_cases"] == 5
    assert saved_report["accuracy"] == 1.0
    assert len(saved_report["results"]) == 5
