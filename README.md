# Banking Policy Assistant — AI Quality Evaluation Framework

A hands-on AI Quality Engineering portfolio project applying software testing principles to a fictional banking-policy assistant.

The project explores how to test a Retrieval-Augmented Generation (RAG) system for **retrieval relevance, answerability, source attribution, groundedness, and appropriate abstention** when evidence is missing or insufficient.

> **Disclaimer:** This is an educational project using synthetic policies and test cases. It is not affiliated with a real bank and must not be used to make real banking decisions.

## Table of Contents

- [Problem Statement](#problem-statement)
- [Quality Engineering Approach](#quality-engineering-approach)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Evaluation Results](#evaluation-results)
- [Run the Project](#run-the-project)
- [Reports and Test Evidence](#reports-and-test-evidence)
- [Repository Structure](#repository-structure)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Skills Demonstrated](#skills-demonstrated)

## Problem Statement

Traditional software tests often check whether an application returns the expected output for a known input. AI-powered applications introduce additional quality risks:

- Relevant policy evidence may not be retrieved.
- Similar questions may produce different retrieval outcomes.
- An assistant may answer when the available evidence is insufficient.
- Generated responses may contain unsupported statements.
- A technically successful response may still be incorrect or poorly grounded.

This project explores how these risks can be converted into repeatable tests and measurable evaluation results.

## Quality Engineering Approach

The framework combines deterministic tests with experiments involving local embedding and language models.

| Quality area | What is evaluated |
|---|---|
| Retrieval relevance | Whether the retriever selects relevant policy evidence |
| Semantic retrieval | Whether embedding-based retrieval handles relevant paraphrases |
| Answerability | Whether the system distinguishes supported from unsupported questions |
| Abstention | Whether weak or missing evidence can trigger a refusal to answer |
| Source attribution | Whether the response identifies the supporting policy evidence |
| Groundedness | Whether generated statements are supported by retrieved evidence |
| Regression testing | Whether automated checks continue to pass after code changes |

### Retrieval strategies

**1. TF-IDF baseline**

A deterministic baseline implemented using scikit-learn. It ranks policy documents against a question and returns a candidate source, evidence, and similarity score.

**2. Embedding-based retrieval**

Uses Ollama's `nomic-embed-text` model to represent policy paragraphs and questions as embeddings, then compares them using cosine similarity.

The current similarity threshold is `0.50`. This is an initial heuristic, not a validated universal cutoff.

**3. RAG and local model evaluation**

The project includes an assistant and local LLM adapter using Ollama and `qwen2.5:1.5b` to experiment with answers based on retrieved policy evidence.

## Architecture

```text
Synthetic banking policies
          |
          v
     Policy retrieval
       /        \
      v          v
  TF-IDF     Embeddings
      \          /
       v        v
    Selected policy evidence
              |
              v
       RAG assistant
              |
              v
      Generated response
              |
              v
  AI quality checks and pytest
              |
              v
      JSON evaluation reports
```

The TF-IDF and embedding retrievers are alternative retrieval approaches. The diagram represents the evaluation workflow conceptually, not a claim that every execution invokes every component.

## Technology Stack

| Area | Tools |
|---|---|
| Programming | Python |
| Automated testing | pytest |
| Baseline retrieval | scikit-learn, TF-IDF |
| Semantic retrieval | Ollama, `nomic-embed-text` |
| Local language model | Ollama, `qwen2.5:1.5b` |
| Evaluation artifacts | JSON reports |
| Version control | Git and GitHub |

## Evaluation Results

The repository's documented development checkpoint reports the following results:

| Evaluation | Recorded result | Dataset / scope |
|---|---:|---|
| TF-IDF retrieval benchmark | 100% | 5 synthetic cases |
| Embedding retrieval benchmark | 100% | 10 synthetic cases |
| Automated pytest suite | 76 passed | Test suite at the recorded checkpoint |

These are historical, project-specific results. They should be re-run before quoting them as the latest results.

**How to interpret them:** A 100% pass rate on a small hand-labelled dataset means the tested cases met their expected outcomes. It does not establish general model accuracy, production readiness, or reliability across unseen banking questions.

The embedding benchmark includes relevant questions, paraphrased questions, and unrelated questions expected to be rejected.

### Evaluation artifacts

The `reports/` directory contains JSON outputs from evaluation runs, including:

- `retrieval_benchmark_report.json`
- `embedding_retrieval_benchmark_report.json`
- `evaluation_report.json`
- `semantic_evaluation_report.json`

Inspect the reports to understand the individual cases and recorded outcomes. Re-run the relevant benchmark before relying on a report as current evidence.

## Run the Project

### Prerequisites

- Python 3.11 or later recommended
- Git, for cloning the repository
- Ollama, for model-backed evaluation
- `nomic-embed-text` for embedding retrieval
- `qwen2.5:1.5b` for local generation and semantic evaluation

Some tests use mocks and do not require Ollama. Model-backed commands require Ollama to be installed, running, and configured with the required models.

### 1. Clone the repository

```powershell
git clone https://github.com/bhavanakathwate/banking-policy-ai-quality.git
cd banking-policy-ai-quality
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use an approved local execution-policy configuration or run the project's commands using the virtual environment's Python executable directly.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Install the local models

Install Ollama from its official website, then run:

```powershell
ollama pull nomic-embed-text
ollama pull qwen2.5:1.5b
```

Ensure the Ollama service is running before executing model-backed commands.

### 5. Run automated tests

```powershell
python -m pytest -v
```

This runs the available pytest suite. Some tests may use mocks, while others may depend on the local environment and installed packages.

### 6. Run the retrieval benchmarks

TF-IDF baseline:

```powershell
python -m app.run_retrieval_benchmark
```

Embedding-based retrieval:

```powershell
python -m app.run_embedding_benchmark
```

### 7. Run AI evaluation

```powershell
python -m app.run_evaluation
python -m app.run_semantic_evaluation
```

### 8. Run the assistant

```powershell
python -m app.run_rag
```

Run commands from the repository root. Check the terminal output and `reports/` directory after each evaluation.

## Reports and Test Evidence

The JSON reports are intended to make evaluation outcomes inspectable rather than relying only on a terminal pass count.

When reviewing a run, examine:

1. The test case and expected outcome.
2. The retrieved policy source and evidence, where recorded.
3. The observed result and whether it matched the expectation.
4. Unsupported or unanswerable questions and how the system handled them.
5. Failures and limitations requiring further investigation.

A passing test demonstrates that a particular assertion succeeded under the tested conditions. It does not by itself prove that a model response is safe or correct in every context.

## Repository Structure

```text
banking-policy-ai-quality/
├── app/
│   ├── assistant.py
│   ├── embedding_retriever.py
│   ├── evaluation.py
│   ├── groundedness.py
│   ├── local_llm_adapter.py
│   ├── rag_assistant.py
│   ├── rag_evaluation.py
│   ├── retriever.py
│   ├── semantic_groundedness.py
│   ├── run_embedding_benchmark.py
│   ├── run_retrieval_benchmark.py
│   ├── run_evaluation.py
│   ├── run_rag.py
│   ├── run_semantic_evaluation.py
│   └── semantic_report.py
├── data/
│   ├── policies/
│   └── test_cases.json
├── reports/
│   ├── embedding_retrieval_benchmark_report.json
│   ├── retrieval_benchmark_report.json
│   ├── evaluation_report.json
│   └── semantic_evaluation_report.json
├── tests/
├── requirements.txt
└── README.md
```

## Limitations

- Policies and evaluation cases are synthetic and limited in scope.
- Benchmark datasets are small and hand-labelled.
- The retrieval similarity threshold requires validation against a larger, representative dataset.
- A high similarity score does not guarantee that retrieved evidence fully answers a question.
- Groundedness checks cover selected failure patterns, not every form of hallucination.
- Embeddings are cached in memory and recomputed in a new process.
- The project has not been validated for production banking use.

## Future Improvements

- Expand the dataset with additional answerable, unanswerable, and paraphrased questions.
- Measure false acceptance and false abstention rates.
- Add more explicit retrieval-quality metrics, such as precision@k and recall@k, where the dataset supports them.
- Add adversarial and regression cases for unsupported claims.
- Improve report comparison across code or configuration changes.
- Integrate automated testing into a CI workflow.
- Test the assistant through a stable API.

These are planned improvements, not claims of completed functionality.

## Skills Demonstrated

Python · pytest · Test automation · Retrieval evaluation · TF-IDF · Embeddings · Cosine similarity · RAG testing · Groundedness evaluation · Local LLM testing · Banking domain QA

---

**Project owner:** Bhavana Kathwate

**Repository:** [banking-policy-ai-quality](https://github.com/bhavanakathwate/banking-policy-ai-quality)
