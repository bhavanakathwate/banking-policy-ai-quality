
from app.local_llm_adapter import generate_answer
from app.retriever import retrieve_policy


def answer_with_rag(question: str) -> dict:
    """Retrieve policy evidence and generate an answer from it."""

    retrieved = retrieve_policy(question)

    if not retrieved["evidence"]:
        return {
            "answer": (
                "I cannot answer because no supporting policy evidence was found."
            ),
            "source": None,
            "abstained": True,
        }

    answer = generate_answer(
        question=question,
        evidence=retrieved["evidence"],
    )

    return {
    "answer": answer,
    "source": retrieved["source"],
    "evidence": retrieved["evidence"],
    "abstained": False,
}
