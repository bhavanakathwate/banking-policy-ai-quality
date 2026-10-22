
import json
from unittest.mock import patch

from app.semantic_report import run_semantic_evaluation


def test_report_records_expected_and_actual_decisions(tmp_path):
    cases = [
        {
            "name": "Supported paraphrase",
            "answer": "Never share your OTP.",
            "expected": True,
        },
        {
            "name": "Unsupported claim",
            "answer": "The bank guarantees every fraud loss.",
            "expected": False,
        },
    ]

    fake_results = [
        {
            "passed": True,
            "reason": "Local semantic evaluator returned: PASS",
        },
        {
            "passed": False,
            "reason": "Local semantic evaluator returned: FAIL",
        },
    ]

    with (
        patch(
            "app.semantic_report.check_semantic_groundedness",
            side_effect=fake_results,
        ),
        patch(
            "app.semantic_report.REPORT_PATH",
            tmp_path / "semantic_evaluation_report.json",
        ),
    ):
        report = run_semantic_evaluation(
            cases,
            "Customers should never share their OTP.",
        )

    assert report["total_cases"] == 2
    assert report["passed_cases"] == 2
    assert report["failed_cases"] == 0
    assert report["pass_rate"] == 1.0

    saved_report = json.loads(
        (tmp_path / "semantic_evaluation_report.json").read_text(
            encoding="utf-8"
        )
    )

    assert saved_report["results"][0]["expected"] is True
    assert saved_report["results"][1]["expected"] is False


def test_report_counts_mismatched_decision_as_failure(tmp_path):
    cases = [
        {
            "name": "Contradictory answer",
            "answer": "Sharing an OTP is safe.",
            "expected": False,
        }
    ]

    fake_result = {
        "passed": True,
        "reason": "Local semantic evaluator returned: PASS",
    }

    with (
        patch(
            "app.semantic_report.check_semantic_groundedness",
            return_value=fake_result,
        ),
        patch(
            "app.semantic_report.REPORT_PATH",
            tmp_path / "semantic_evaluation_report.json",
        ),
    ):
        report = run_semantic_evaluation(
            cases,
            "Customers should never share their OTP.",
        )

    assert report["total_cases"] == 1
    assert report["passed_cases"] == 0
    assert report["failed_cases"] == 1
    assert report["pass_rate"] == 0.0
