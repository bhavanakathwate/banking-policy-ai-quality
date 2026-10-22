"""Evaluation helpers for the Banking Policy Assistant starter project."""
from pathlib import Path
import json
from app.assistant import answer_question

ROOT = Path(__file__).resolve().parents[1]
TEST_CASES_PATH = ROOT / "data" / "test_cases.json"

def calculate_coverage(matched_terms, required_terms):
    if len(required_terms) == 0:
        return 1.0

    return len(matched_terms) / len(required_terms)


matched_terms = ["otp", "bank employee"]
required_terms = ["never share", "otp", "bank employee"]

coverage = calculate_coverage(matched_terms, required_terms)

print(f"Coverage: {coverage:.2f}")

if coverage >= 0.80:
    print("PASS")
else:
    print("FAIL")