from agents.base import Agent
import json

SYSTEM_PROMPT = """你是一个ADAS日志分析专家。你的任务是分析传感器日志，找出异常模式。

    分析要点：
    1. 错误类型：识别错误码、异常类型（如通信中断、数据越界、超时等）
    2. 时间模式：是否有周期性异常、突发异常
    3. 影响范围：影响哪些传感器、哪些功能模块
    4. 严重程度：轻微/中等/严重/致命

    输出格式（JSON）：
    {
        "thinking": "你的分析思路",
        "error_type": "错误类型",
        "time_pattern": "时间模式",
        "impact_scope": "影响范围",
        "severity": "严重程度",
        "suggestion": "建议处理"
    }

    只输出JSON，不要输出其他内容。"""

class LogAgent(Agent):
    def __init__(self, model_adapter, message_bus, store):
        super().__init__(model_adapter, message_bus, store)
    
    def process(self, message):
        prompt = message.content
        result = self.model_adapter.chat(prompt,SYSTEM_PROMPT)
        data = json.loads(result)
        return data