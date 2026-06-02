from agents.base import Agent
from core.model_adapter import extract_json
import json

SYSTEM_PROMPT = """你是一个ADAS日志分析专家。你的任务是分析传感器日志，找出异常模式。

    要求：
    1. 只基于提供的知识库文档内容进行分析，不要凭自身知识编造
    2. 如果文档中没有相关信息，在suggestion字段中明确告知用户

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
    def __init__(self, model_adapter, store):
        super().__init__(model_adapter, store)

    def process(self, message):
        docs = self.store.retrieve(message.content)
        doc_text = "\n".join([d["content"] for d in docs])
        prompt = f"用户问题：{message.content}\n\n知识库文档：\n{doc_text}"
        result = self.model_adapter.chat(prompt, SYSTEM_PROMPT)
        try:
            data = json.loads(extract_json(result))
        except json.JSONDecodeError:
            data = {
                "thinking": "LLM 返回格式错误",
                "error_type": "未知",
                "time_pattern": "未知",
                "impact_scope": "未知",
                "severity": "未知",
                "suggestion": "系统暂时无法分析，请稍后再试"
            }
        data["sources"] = docs
        return data