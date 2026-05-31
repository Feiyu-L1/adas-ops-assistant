from abc import ABC, abstractmethod 

class ModelAdapter:

    @abstractmethod
    def chat(self, prompt):
        pass