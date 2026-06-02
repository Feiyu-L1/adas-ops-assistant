from agents.base import Agent
from core.model_adapter import extract_json
import json

SYSTEM_PROMPT = """你是一个ADAS技术文档专家。根据检索到的文档内容，回答用户的问题。

    要求：
    1. 只基于提供的文档内容回答，不要编造
    2. 如果文档中没有相关信息，明确告知用户
    3. 回答要简洁准确
    
     输出格式（JSON）：
    {
        "thinking": "你的分析思路",
        "answer": "回答内容"
    }

    只输出JSON，不要输出其他内容。"""

class DocAgent(Agent):
    def __init__(self, model_adapter, store):
        super().__init__(model_adapter, store)
    
    def process(self, message):
        docs = self.store.retrieve(message.content)
        doc_text = "\n".join([d["content"] for d in docs])
        prompt = f"用户问题：{message.content}\n\n相关文档:\n{doc_text}"
        result = self.model_adapter.chat(prompt,SYSTEM_PROMPT)
        try:
            data = json.loads(extract_json(result))
        except json.JSONDecodeError:
            data = {
                "thinking": "LLM 返回格式错误",
                "answer": "抱歉，系统暂时无法处理您的请求。"
            }
        data["sources"] = docs
        return data