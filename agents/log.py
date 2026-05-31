from agents.base import Agent

SYSTEM_PROMPT = """你是一个ADAS日志分析专家。你的任务是分析传感器日志，找出异常模式。

    分析要点：
    1. 错误类型：识别错误码、异常类型（如通信中断、数据越界、超时等）
    2. 时间模式：是否有周期性异常、突发异常
    3. 影响范围：影响哪些传感器、哪些功能模块
    4. 严重程度：轻微/中等/严重/致命

    输出格式：
    - 错误类型：xxx
    - 时间模式：xxx
    - 影响范围：xxx
    - 严重程度：xxx
    - 建议处理：xxx"""

class LogAgent(Agent):
    def __init__(self, model_adapter, message_bus, store):
        super().__init__(model_adapter, message_bus, store)
    
    def process(self, message):
        prompt = message.content
        result = self.model_adapter.chat(prompt,SYSTEM_PROMPT)
        return result