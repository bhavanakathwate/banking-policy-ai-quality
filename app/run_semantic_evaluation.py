
from app.semantic_groundedness import check_semantic_groundedness
from app.semantic_report import run_semantic_evaluation


EVIDENCE = """
Customers should never share their one-time password (OTP), PIN,
or password with anyone, including a bank employee.

If a customer suspects unauthorized account access, they should
immediately use the official banking app or the verified
customer-support channel to secure the account.

The bank will never ask a customer to disclose their full password
or OTP over a phone call, email, or chat.

Customers should review account activity regularly and report
unfamiliar transactions through the official support channel.
"""


TEST_CASES = [
    {
        "name": "Supported paraphrase",
        "answer": (
            "Never disclose your OTP, PIN, or password to bank staff."
        ),
        "expected": True,
    },
    {
        "name": "Unsupported reimbursement promise",
        "answer": (
            "The bank guarantees reimbursement for every fraud loss."
        ),
        "expected": False,
    },
    {
        "name": "Contradictory OTP advice",
        "answer": (
            "Customers can safely share their OTP with a bank employee."
        ),
        "expected": False,
    },
    {
        "name": "Supported policy summary",
        "answer": (
            "Customers should not share OTPs with bank employees and "
            "should use official channels if they suspect unauthorized access."
        ),
        "expected": True,
    },
        {
        "name": "Unsupported account unlock promise",
        "answer": "The bank will unlock any blocked account within one hour.",
        "expected": False,
    },
    {
        "name": "Supported unauthorized access guidance",
        "answer": "If you suspect unauthorized access, use the official banking app or verified customer support to secure your account.",
        "expected": True,
    },
    {
        "name": "Partially supported answer with unsupported promise",
        "answer": "Never share your OTP with bank employees. The bank guarantees full compensation for every fraudulent transaction.",
        "expected": False,
    },
    {
        "name": "Unsupported transaction reversal guarantee",
        "answer": "Reporting an unfamiliar transaction guarantees that the money will be returned.",
        "expected": False,
    },
    {
        "name": "Supported suspicious transaction reporting",
        "answer": "Customers should regularly review account activity and report unfamiliar transactions through official support.",
        "expected": True,
    },
    {
        "name": "Unsupported request for full password",
        "answer": "Customers should send their full password to customer support by email to verify their identity.",
        "expected": False,
    },
]

def main():
    report = run_semantic_evaluation(TEST_CASES, EVIDENCE)

    print("\nSemantic evaluation report")
    print(f"Total cases: {report['total_cases']}")
    print(f"Matched expected decisions: {report['passed_cases']}")
    print(f"Failed cases: {report['failed_cases']}")
    print(f"Pass rate: {report['pass_rate']:.0%}")
    print("Report: reports/semantic_evaluation_report.json")



if __name__ == "__main__":
    main()
