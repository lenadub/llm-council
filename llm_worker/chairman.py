import os
import time
import httpx
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1:8b")
OLLAMA_URL = "http://localhost:11434/api/chat"

app = FastAPI(title="LLM Chairman", version="1.0")


class SynthesisRequest(BaseModel):
    user_query: str
    stage1_results: list
    stage2_results: list


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}


@app.post("/synthesize")
async def synthesize(req: SynthesisRequest):
    start = time.time()

    stage1_text = "\n\n".join(
        f"Model: {r['model']}\nResponse: {r['response']}"
        for r in req.stage1_results
    )

    stage2_text = "\n\n".join(
        f"Model: {r['model']}\nRanking:\n{r['ranking']}"
        for r in req.stage2_results
    )

    prompt = f"""
You are the Chairman of an LLM Council.

Original Question:
{req.user_query}

STAGE 1 - Individual Responses:
{stage1_text}

STAGE 2 - Peer Rankings:
{stage2_text}

Your task:
Synthesize all of the above into a single, clear, accurate, well-structured final answer.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    async with httpx.AsyncClient(timeout=180) as client:
        r = await client.post(OLLAMA_URL, json=payload)
        r.raise_for_status()
        data = r.json()

    return {
        "content": data["message"]["content"],
        "latency_ms": int((time.time() - start) * 1000)
    }