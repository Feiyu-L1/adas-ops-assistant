# ADAS Ops Assistant

> An intelligent, multi-agent operations assistant for Advanced Driver Assistance Systems (ADAS), powered by LangGraph and retrieval-augmented generation.

---

## Overview

ADAS Ops Assistant is an AI-powered Q&A system designed to help engineers diagnose and resolve ADAS operational issues — from sensor anomalies and log analysis to configuration guidance and fault escalation. Users submit a maintenance query in natural language; the system automatically classifies intent, routes to the appropriate agent pipeline, and returns a structured response with cited sources.

The project demonstrates a practical application of agentic LLM architectures in a safety-critical vertical domain, built with a model-agnostic adapter layer for easy backend switching.

---

## Architecture

```
User Input
    ↓
TriageAgent  (intent classification)
    ├── Log anomaly / Performance issue  →  LogAgent  →  ResponseAgent  →  EscalationAgent
    └── Configuration / General query   →  DocAgent
```

The entire pipeline is orchestrated by a **LangGraph StateGraph**. Knowledge retrieval is powered by **Dify** (supports keyword, full-text, and semantic search).

---

## Agent Roles

| Agent | Responsibility |
|---|---|
| `TriageAgent` | Classifies incoming query intent and routes to the correct pipeline |
| `LogAgent` | Analyses log patterns and identifies anomalies |
| `DocAgent` | Retrieves answers from the ADAS knowledge base |
| `ResponseAgent` | Generates a structured fault report |
| `EscalationAgent` | Determines whether the issue requires human escalation |

---

## Tech Stack

- **Python 3.11+**
- **LangGraph** — stateful multi-agent orchestration
- **Streamlit** — web frontend
- **Dify** — knowledge base & RAG retrieval
- Model-agnostic adapter (currently supports Mimo; OpenAI integration in progress)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Feiyu-L1/adas-ops-assistant.git
cd adas-ops-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
MIMO_API_KEY=your_mimo_api_key
DIFY_API_KEY=your_dify_api_key
DIFY_DATASET_ID=your_dify_dataset_id
USE_DIFY_STORE=true
DIFY_SEARCH_METHOD=keyword_search   # keyword_search | full_text_search | semantic_search
```

**Search method options:**

| Value | Description |
|---|---|
| `keyword_search` | Keyword matching — no extra setup required (default) |
| `full_text_search` | Full-text search — better for Chinese content |
| `semantic_search` | Semantic/vector search — best quality, requires an Embedding model configured in Dify |

### 4. Set up Dify knowledge base

Create a knowledge base in [Dify](https://dify.ai), upload your ADAS documentation (sensor manuals, fault handling specs, etc.), and paste the dataset ID into `.env`.

### 5. Run

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## Running Without Dify

Set `USE_DIFY_STORE=false` in `.env` to use the built-in `MockStore` — a lightweight in-memory store with simple keyword matching. Suitable for local development and testing without external dependencies.

---

## Project Structure

```
adas-ops-assistant/
├── app.py                  # Streamlit frontend
├── config.py               # Model & knowledge base configuration
├── agents/
│   ├── base.py             # Abstract base class for all agents
│   ├── triage.py           # Intent classification
│   ├── log.py              # Log anomaly analysis
│   ├── doc.py              # Documentation Q&A
│   ├── response.py         # Fault report generation
│   └── escalation.py       # Escalation decision logic
├── core/
│   ├── graph.py            # LangGraph state machine
│   ├── model_adapter.py    # LLM provider adapter layer
│   ├── knowledge_store.py  # Knowledge store (Mock / Dify)
│   └── message.py          # Message data structures
└── tests/                  # Unit tests
```

---

## Roadmap

- [ ] OpenAI GPT-4o backend integration
- [ ] OpenAI Assistants API for persistent conversation threads
- [ ] Structured benchmarking on ADAS fault diagnosis tasks
- [ ] Expanded ADAS documentation coverage
- [ ] Improved multi-turn dialogue handling

---

## Contributing

Issues and pull requests are welcome. If you work in the autonomous vehicle or ADAS domain and have relevant documentation or test cases to contribute, please open an issue to discuss.

---

## License

MIT
