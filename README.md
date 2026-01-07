
# LLM Council — Local & Distributed Deployment

## Group Information

**TD Group:** `CDOF2`

**Team Members:**

* DOGUET Cassie
* DUBOIS Léna
* LALEYE Nadirath
* MAARBANI Yasmine

---

## Project Overview

This project is a **local and distributed reimplementation of Andrej Karpathy’s LLM Council concept**.
Instead of relying on cloud-based LLM APIs, the entire system runs **locally**, using multiple Large Language Models deployed across **separate machines** and coordinated via **REST APIs**.

The application provides a web interface similar to ChatGPT, but under the hood it leverages **multiple local LLMs working together**. Each model contributes an independent perspective, reviews the others’ outputs, and a dedicated **Chairman LLM** synthesizes a final answer.

This architecture emphasizes:

* diversity of reasoning
* self-critique
* aggregation of perspectives
* distributed system design

---

## What Is the LLM Council?

Rather than querying a single LLM, user queries are processed by a **Council of LLMs** operating in three stages:

### **Stage 1 — First Opinions**

* The user submits a query.
* Each council LLM generates an answer **independently**.
* Responses are displayed side-by-side in a tabbed interface for inspection.

### **Stage 2 — Peer Review & Ranking**

* Each LLM reviews the other responses.
* Model identities are **anonymized at the prompt level** to avoid bias.
* Each LLM evaluates the responses based on accuracy and insight and produces a ranking.

### **Stage 3 — Chairman Synthesis**

* A designated **Chairman LLM**, running as a **separate service**, receives:

  * all Stage 1 responses
  * all Stage 2 rankings
* The Chairman synthesizes these into a single, final answer presented to the user.

---

## Key Differences from the Original Project

| Original Implementation | This Project                           |
| ----------------------- | -------------------------------------- |
| Cloud-based LLMs        | Fully local LLMs                       |
| OpenRouter API          | Ollama-based local inference           |
| Single-machine focus    | Distributed multi-machine architecture |
| No service separation   | Separate Workers & Chairman services   |

All cloud-based APIs have been **completely removed**.

---

## System Architecture

```
Browser
   |
Frontend (React)
   |
Backend (FastAPI Orchestrator)
   |
   |── Worker 1 (PC A, local LLM)
   |── Worker 2 (PC B, local LLM)
   |── Worker 3 (PC C, local LLM)
   |
   └── Chairman (PC D, synthesis-only LLM)
```

* **Workers** generate first opinions and peer rankings.
* **Chairman** performs synthesis only.
* All components communicate using **REST APIs**.
* Ollama runs **locally on each machine**.

---

## Network & IP Address Configuration (IMPORTANT)

This project relies on **explicit IP address configuration** to enable communication between machines.

### Requirements

* All machines must be reachable over the network (same LAN or private VPN).
* Each Worker and the Chairman expose a REST API on a known port.
* The Backend must know the **IP address of each Worker and the Chairman**.

### Example Worker Configuration (`backend/worker_provider.py`)

```python
WORKERS = [
    {"name": "llama3.1-8b", "url": "http://192.168.1.10:8002/chat"},
    {"name": "mistral", "url": "http://192.168.1.42:8002/chat"},
    {"name": "qwen2.5-7b", "url": "http://192.168.1.43:8002/chat"},
]

CHAIRMAN_URL = "http://192.168.1.50:9000/synthesize"
```

Each team member running a Worker must provide:

* their **local IP address**
* the **model name** they are hosting

---

## Local LLM Stack

* **Inference engine:** Ollama
* **Worker models (example):**

  * `llama3.1:8b`
  * `mistral`
  * `qwen2.5:7b`
* **Chairman model (example):**

  * `llama3.1:8b`

Each Worker runs the **same service code**, configured via environment variables to select a different model.

---

## Setup & Installation

### 1. Backend Dependencies

```bash
pip install uv
uv sync
```

---

### 2. Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

---

### 3. No API Keys Required

* ❌ No OpenRouter
* ❌ No OpenAI
* ❌ No cloud credentials

All inference runs **locally**.

---

## Running the Application

### **Worker Nodes (one per machine)**

```bash
cd llm_worker
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn httpx
```

Set the model:

```bash
set MODEL_NAME=mistral   # Windows
```
```bash
export MODEL_NAME=mistral   # Linux/macOS
```

Run the Worker:

```bash
uvicorn worker:app --host 0.0.0.0 --port 8002
```

---

### **Chairman Node (separate service)**

```bash
cd llm_worker
set MODEL_NAME=qwen2.5:7b
uvicorn chairman:app --host 0.0.0.0 --port 9000
```

---

### **Backend (Orchestrator)**

```bash
uv run python -m backend.main
```

Backend runs on:

```
http://localhost:8001
```

---

### **Frontend**

```bash
cd frontend
npm run dev
```

Open:

```
http://localhost:5173
```

---

## Demo Workflow

1. Start all Worker services
2. Start Chairman service
3. Start Backend
4. Start Frontend
5. Submit a query
6. Observe:

   * Stage 1 individual responses
   * Stage 2 peer rankings
   * Stage 3 Chairman synthesis

---

## Tech Stack

* **Backend:** FastAPI (Python 3.10+), async httpx
* **Frontend:** React + Vite
* **Inference:** Ollama (local LLMs)
* **Architecture:** Distributed REST services
* **Storage:** JSON files in `data/conversations/`
* **Package Management:** uv (Python), npm (JavaScript)

---

## Notes on Anonymization

* Model identities are anonymized **at the prompt level** during peer review to prevent bias.
* Model names remain visible in the UI for transparency and inspection.

---

## Inspiration & Credits

This project is inspired by Andrej Karpathy’s original **LLM Council** concept.
The implementation has been heavily refactored for **local execution**, **distributed deployment**, and **educational purposes**.
