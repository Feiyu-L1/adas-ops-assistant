from agents.base import Agent

SYSTEM_PROMPT = """你是一个ADAS故障报告专家。根据提供的分析信息，生成结构化的故障报告。

    报告格式：
    故障报告
    - 问题描述：xxx
    - 根因分析：xxx
    - 影响范围：xxx
    - 严重程度：xxx
    - 处理建议：xxx
    - 预防措施：xxx

    要求：简洁、专业、可执行。"""

class ResponseAgent(Agent):
    def __init__(self, model_adapter, message_bus, store):
        super().__init__(model_adapter, message_bus, store)
    
    def process(self, message):
        prompt = message.content
        result = self.model_adapter.chat(prompt, SYSTEM_PROMPT)
        return result