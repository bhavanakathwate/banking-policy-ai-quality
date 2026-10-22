import json
from unittest.mock import patch

from app import run_retrieval_benchmark as benchmark

def test_retrieval_metrics_calculate_correctly():
    results = [
        {
            "expected_source": "account_security.md",
            "actual_source": "account_security.md",
        },
        {
            "expected_source": "card_disputes.md",
            "actual_source": "account_security.md",
        },
        {
            "expected_source": "account_security.md",
            "actual_source": None,
        },
        {
            "expected_source": None,
            "actual_source": None,
        },
        {
            "expected_source": None,
            "actual_source": "card_disputes.md",
        },
    ]

    metrics = benchmark.calculate_retrieval_metrics(results)

    assert metrics["answerable_cases"] == 3
    assert metrics["unsupported_cases"] == 2
    assert metrics["correct_retrievals"] == 1
    assert metrics["wrong_sources"] == 1
    assert metrics["false_abstentions"] == 1
    assert metrics["false_acceptances"] == 1
    assert metrics["correct_abstentions"] == 1

    assert metrics["correct_retrieval_rate"] == 0.333
    assert metrics["wrong_source_rate"] == 0.333
    assert metrics["false_abstention_rate"] == 0.333
    assert metrics["false_acceptance_rate"] == 0.5
    assert metrics["correct_abstention_rate"] == 0.5


def test_retrieval_metrics_handle_empty_results():
    metrics = benchmark.calculate_retrieval_metrics([])

    assert metrics["answerable_cases"] == 0
    assert metrics["unsupported_cases"] == 0
    assert metrics["correct_retrieval_rate"] == 0.0
    assert metrics["wrong_source_rate"] == 0.0
    assert metrics["false_abstention_rate"] == 0.0
    assert metrics["false_acceptance_rate"] == 0.0
    assert metrics["correct_abstention_rate"] == 0.0