from abc import ABC, abstractmethod 
import os
from openai import OpenAI

class ModelAdapter(ABC):

    @abstractmethod
    def chat(self, prompt, system_prompt="你是一个AI助手"):
        pass

class MimoAdapter(ModelAdapter):
    def __init__(self, api_key, model, base_url="https://token-plan-sgp.xiaomimimo.com/v1"):
        self.client = OpenAI(
            api_key = api_key,
            base_url = base_url
        )
        self.model = model
    
    def chat(self, prompt,system_prompt="你是一个AI助手"):
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
      