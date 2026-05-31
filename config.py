import os
from dotenv import load_dotenv
from core.model_adapter import MimoAdapter

load_dotenv()

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