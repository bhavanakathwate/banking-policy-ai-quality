# Banking Policy Assistant - AI Quality Evaluation Framework

A portfolio project demonstrating **AI quality engineering, retrieval evaluation, groundedness checks, and automated testing** for a fictional banking-policy assistant.

The project uses synthetic policy documents and local models to explore how a retrieval-augmented generation (RAG) system can find relevant evidence, handle unsupported questions, and be evaluated systematically.

> **Disclaimer:** This is an educational portfolio project using fictional policies. It is not affiliated with a real bank and must not be used for real banking decisions.

## Project goals

- Apply established QA practices to AI-assisted systems.
- Compare keyword-based and semantic retrieval approaches.
- Evaluate source selection against labeled test cases.
- Test abstention when evidence is missing or retrieval confidence is low.
- Check generated responses for unsupported claims and promises.
- Use automated tests and measurable evaluation reports to identify failures.

## Current capabilities

### 1. TF-IDF retrieval baseline

`app/retriever.py` implements a TF-IDF-based document retriever using scikit-learn. It ranks policy documents against a question and returns the best source, evidence, and similarity score.

### 2. Embedding-based retrieval

`app/embedding_retriever.py` uses Ollama's `nomic-embed-text` model to embed policy paragraphs and compare them with questions using cosine similarity.

- Returns the source policy and the most relevant paragraph.
- Uses an initial similarity threshold of `0.50` to reject weak matches.
- Caches paragraph embeddings in memory within a running Python process.

### 3. RAG assistant and local model integration

The project includes a local LLM adapter and RAG assistant components for experimenting with answer generation based on retrieved policy evidence. The local model setup uses Ollama and `qwen2.5:1.5b`.

### 4. AI quality evaluation

The evaluation code and tests cover retrieval behavior, expected answers, source attribution, abstention, and groundedness checks, including detection of selected unsupported promises.

### 5. Benchmark reports

The repository includes JSON reports for retrieval and evaluation runs. These reports help make the evaluation results inspectable and reproducible.

## Current benchmark results

The latest recorded results from the development environment are:

| Evaluation | Result | Test set |
|---|---:|---:|
| TF-IDF retrieval benchmark | 100% | 5 cases |
| Embedding retrieval benchmark | 100% | 10 cases |
| Automated pytest suite | 76 passed | Existing test suite at the last checkpoint |

These results are from small, hand-labeled synthetic test sets. They demonstrate that the current implementation passes these specific cases; they do **not** establish production-level accuracy or general reliability.

The embedding benchmark includes relevant banking questions, paraphrased questions, and unrelated questions that should be rejected. The similarity threshold is an initial heuristic and requires validation on a larger dataset.

## Repository structure

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
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.11 or later recommended.
- Git, if you want to clone the repository.
- Ollama for embedding retrieval and local LLM evaluation.
- The `nomic-embed-text` embedding model.
- The `qwen2.5:1.5b` model for local answer generation and semantic evaluation.

Some unit tests use mocks and do not require a running Ollama instance. Model-backed benchmark commands require Ollama to be running with the relevant model installed.

## Setup

### 1. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Python dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install Ollama models

Install Ollama from its official website, then run:

```powershell
ollama pull nomic-embed-text
ollama pull qwen2.5:1.5b
```

Make sure Ollama is running before starting model-backed commands.

## Running the project

Run commands from the repository root.

### Run automated tests

```powershell
python -m pytest -v
```

### Run the TF-IDF retrieval benchmark

```powershell
python -m app.run_retrieval_benchmark
```

### Run the embedding retrieval benchmark

```powershell
python -m app.run_embedding_benchmark
```

### Run semantic evaluation

```powershell
python -m app.run_semantic_evaluation
```

### Run the RAG assistant

```powershell
python -m app.run_rag
```

Generated evaluation reports are written to the `reports/` directory.

## Limitations and next steps

- The policy documents and benchmark questions are synthetic and limited in scope.
- The benchmarks are small and hand-labeled.
- A similarity threshold alone cannot establish that retrieved evidence fully answers a question.
- Groundedness checks cover selected failure patterns and are not a complete safety guarantee.
- Paragraph embeddings are cached only in memory, so a new process recomputes them.
- The project has not been validated for production banking use.

Potential next steps include expanding the benchmark dataset, evaluating false positives and false abstentions, improving embedding-cache persistence, adding CI, and testing the assistant through a stable API.

## Skills demonstrated

**Python · pytest · QA automation · Retrieval evaluation · TF-IDF · Embeddings · Cosine similarity · RAG testing · Groundedness evaluation · Ollama · Banking domain testing**
