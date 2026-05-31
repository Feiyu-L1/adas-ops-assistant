from core.model_adapter import MimoAdapter
from dotenv import load_dotenv
import os

load_dotenv()
api_key =os.environ.get("MIMO_API_KEY")
adapter = MimoAdapter(
    api_key=api_key, 
    model="mimo-v2.5-pro",
    base_url="https://token-plan-sgp.xiaomimimo.com/v1")

response = adapter.chat(prompt="你好，介绍一下自己",system_prompt="你是 ADAS 智能运维助手，专门负责自动驾驶系统的故障排查。")
print(response)
