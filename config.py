import os
from dotenv import load_dotenv
from core.model_adapter import MimoAdapter

load_dotenv(override=True)

def get_triage_adapter():
    """Lightweight model for intent classification"""
    return MimoAdapter(
        api_key=os.getenv("MIMO_API_KEY"),
        model="mimo-v2.5"
    )

def get_adapter():
    """Powerful model for complex reasoning"""
    return MimoAdapter(
        api_key=os.getenv("MIMO_API_KEY"),
        model="mimo-v2.5-pro"
    )

DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_DATASET_ID = os.getenv("DIFY_DATASET_ID")
USE_DIFY_STORE = os.getenv("USE_DIFY_STORE", "false").lower() == "true"