from agents.base import Agent
import json

SYSTEM_PROMPT = """你是一个ADAS智能运维助手。你的任务是判断用户的问题属于哪种意图。

    意图类别：
    1. 日志异常 - 传感器日志报错、数据异常、通信中断等
    2. 性能问题 - 响应延迟、处理速度慢、资源占用高等
    3. 配置问题 - 参数配置、阈值设置、系统配置等
    4. 常规问题 - 使用咨询、功能说明、操作指南等

    输出格式（JSON）：
    {
        "thinking": "你的思考过程",
        "intent": "意图类别"
    }

    只输出JSON，不要输出其他内容。"""

class TriageAgent(Agent):
    def __init__(self, model_adapter, message_bus, store):
        super().__init__(model_adapter, message_bus, store)

    def process(self,message):
        prompt = message.content
        result = self.model_adapter.chat(prompt,SYSTEM_PROMPT)

        data = json.loads(result)
        return data