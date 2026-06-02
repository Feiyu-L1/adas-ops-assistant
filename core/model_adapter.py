from abc import ABC, abstractmethod
import os
from openai import OpenAI
import time
import json

def extract_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()

class ModelAdapter(ABC):

    @abstractmethod
    def chat(self, prompt, system_prompt="你是一个AI助手"):
        pass

class MimoAdapter(ModelAdapter):
    def __init__(self, api_key, model, base_url="https://token-plan-cn.xiaomimimo.com/v1"):
        self.client = OpenAI(
            api_key = api_key,
            base_url = base_url
        )
        self.model = model
    
    def chat(self, prompt,system_prompt="你是一个AI助手"):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}],
                    max_completion_tokens=2048,
                    temperature=1.0,
                    top_p=0.95,
                    stream=False
            )
                return completion.choices[0].message.content
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1)  
                    continue
                else:
                    return json.dumps({
                    "thinking": f"API调用失败: {str(e)}",
                    "intent": "未知",
                    "answer": "抱歉，系统暂时无法处理您的请求，请稍后再试。"
                })
      