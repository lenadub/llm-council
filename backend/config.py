"""
Configuration for the LLM Council (Local Deployment).
"""

# Council models are now logical names (not cloud IDs)
COUNCIL_MODELS = [
    "llama3.1-8b"
]

# Chairman model (logical name)
CHAIRMAN_MODEL = "llama3.1-8b"

# Data directory for conversation storage
DATA_DIR = "data/conversations"