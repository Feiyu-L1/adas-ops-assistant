from agents.base import Agent
from unittest.mock import MagicMock

class TestAgent(Agent):
    def process(self,message):
        return "已收到" + message #Add the message content to the return

def test_receive():
    fake_adapter = None
    fake_bus = MagicMock()
    fake_store = None
    agent = TestAgent(fake_adapter, fake_bus, fake_store)

    agent.receive("测试消息")
    fake_bus.publish.assert_called_once()
    fake_bus.publish.assert_called_with("已收到测试消息")
    print(fake_bus.publish.call_args)

   