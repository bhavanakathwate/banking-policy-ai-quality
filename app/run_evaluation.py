"""Run all evaluation cases and write a JSON report."""
from pathlib import Path
import json
from app.evaluation import build_report

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "reports" / "evaluation_report.json"


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Evaluation complete.")
    print(json.dumps(report["metrics"], indent=2))
    print(f"Full report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
