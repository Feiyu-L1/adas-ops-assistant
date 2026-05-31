from abc import ABC, abstractmethod

class Agent(ABC):
    # Initialize the agent
    def __init__(self, model_adapter, message_bus, store):
        self.model_adapter = model_adapter
        self.message_bus = message_bus
        self.store = store
    # Receive message,process it and send the result
    def receive(self, message): 
        result = self.process(message)
        self.send(result)

    # Force different agents to override different methods to process message
    @abstractmethod 
    def process(self, message):
        pass
    
    # Send the processed message to the message bus
    def send(self, result): 
        self.message_bus.publish(result)
    
    