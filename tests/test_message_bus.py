from core.message_bus import MessageBus
from core.message import Message

def test_subscribe():
    mb = MessageBus()
    fake_agent1 = "fake agent"
    mb.subscribe("log_analysis", fake_agent1)
    assert "log_analysis" in mb.subscribe_list
    assert fake_agent1 in mb.subscribe_list["log_analysis"]