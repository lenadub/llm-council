import os
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import time

MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1:8b")
OLLAMA_URL = "http://localhost:11434/api/chat"

app = FastAPI()

class ChatRequest(BaseModel):
    messages: list
    temperature: float = 0.7
    max_tokens: int = 512

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}

@app.post("/chat")
async def chat(req: ChatRequest):
    start = time.time()
    payload = {
        "model": MODEL_NAME,
        "messages": req.messages,
        "stream": False
    }

    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(OLLAMA_URL, json=payload)
        r.raise_for_status()
        data = r.json()

    return {
        "content": data["message"]["content"],
        "latency_ms": int((time.time() - start) * 1000)
    }