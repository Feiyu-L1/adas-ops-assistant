class MessageBus:
    def __init__(self):
        self.subscribe_list = {}

    def subscribe(self, message_type, agent):
        if message_type in self.subscribe_list:
            self.subscribe_list[message_type].append(agent)
        else:
            self.subscribe_list[message_type] = [agent]
    
    def publish(self,message):
        message_type = message.type
        if message_type in self.subscribe_list:
            for agent in self.subscribe_list[message_type]:
                agent.receive(message)
            