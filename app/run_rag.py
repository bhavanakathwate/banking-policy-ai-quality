
from app.rag_assistant import answer_with_rag
from app.rag_evaluation import evaluate_rag_result
from app.groundedness import check_groundedness


def main():
    # Step 1: Ask a banking policy question.
    question = (
        "Should a customer share their OTP with someone claiming "
        "to be a bank employee?"
    )

    # Step 2: Retrieve policy evidence and generate an answer.
    result = answer_with_rag(question)

    # Step 3: Evaluate the generated response.
    evaluation = evaluate_rag_result(result)

    # Step 4: Print the question and generated answer.
    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(result["answer"])

    # Step 5: Print the source and evidence used by the assistant.
    print("\nSource:")
    print(result.get("source"))

    print("\nEvidence:")
    print(result.get("evidence", ""))

    print("\nAbstained:")
    print(result.get("abstained"))

    # Step 6: Print the quality evaluation.
    print("\nQuality evaluation:")
    for metric, value in evaluation.items():
        print(f"{metric}: {value}")

    # Step 7: Diagnose the groundedness result.
    groundedness_detail = check_groundedness(
        result.get("answer", ""),
        result.get("evidence", ""),
    )

    print("\nGroundedness diagnostic:")
    print("Answer:", result.get("answer", ""))
    print("Evidence:", result.get("evidence", ""))
    print("Reason:", groundedness_detail["reason"])


if __name__ == "__main__":
    main()
