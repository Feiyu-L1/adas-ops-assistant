from agents.base import Agent

SYSTEM_PROMPT = """你是一个ADAS运维升级判断专家。根据故障报告，判断是否需要人工介入。

    判断规则：
    - 轻微/中等 → 不需要升级，系统自动处理
    - 严重/致命 → 需要升级，通知运维人员

    只输出"需要升级"或"不需要升级"，不要输出其他内容。"""

class EscalationAgent(Agent):
    def __init__(self, model_adapter, message_bus, store):
        super().__init__(model_adapter, message_bus, store)
    
    def process(self, message):
        prompt = message.content
        result = self.model_adapter.chat(prompt,SYSTEM_PROMPT)
        return result
    