import asyncio
import httpx
from typing import List, Dict, Any

# For now: ONE worker (yours)
# Later: each teammate adds their own worker here

CHAIRMAN_URL = "http://localhost:9000/synthesize"

WORKERS = [
    {
        "name": "llama3.1-8b",
        "url": "http://192.168.1.10:8002/chat"
    },
    {
        "name": "mistral",
        "url": "http://192.168.1.42:8002/chat"
    },
    {
        "name": "qwen2.5-7b",
        "url": "http://192.168.1.43:8002/chat"
    }
]



async def query_worker(worker, messages, temperature=0.7, max_tokens=512):
    payload = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    async with httpx.AsyncClient(timeout=180) as client:
        response = await client.post(worker["url"], json=payload)
        response.raise_for_status()
        data = response.json()

    return {
        "content": data["content"],
        "latency_ms": data.get("latency_ms")
    }


async def query_models_parallel(
    models: List[str],   # ignored, kept for compatibility
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 512
) -> Dict[str, Any]:
    """
    Drop-in replacement for openrouter.query_models_parallel
    """
    tasks = [
        query_worker(worker, messages, temperature, max_tokens)
        for worker in WORKERS
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    responses = {}
    for worker, result in zip(WORKERS, results):
        if isinstance(result, Exception):
            responses[worker["name"]] = None
        else:
            responses[worker["name"]] = result

    return responses


async def query_model(
    model: str,
    messages: list,
    temperature: float = 0.7,
    max_tokens: int = 512,
    timeout: float = 180.0
):
    # Extract structured data from chairman prompt
    import json

    # The prompt is already structured in council.py
    payload = {
        "user_query": messages[0]["content"],
        "stage1_results": [],
        "stage2_results": []
    }

    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(CHAIRMAN_URL, json=payload)
        r.raise_for_status()
        data = r.json()

    return {"content": data["content"]}