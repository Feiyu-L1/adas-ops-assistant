from abc import ABC, abstractmethod

class Agent(ABC):
    def __init__(self, model_adapter, store):
        self.model_adapter = model_adapter
        self.store = store

    @abstractmethod
    def process(self, message):
        pass
    
    