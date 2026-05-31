from unittest.mock import MagicMock
from core.message import Message
from agents.triage import TriageAgent

def test_triage_process():
    mock_adapter = MagicMock()
    mock_adapter.chat.return_value = "日志异常"

    agent = TriageAgent(
        model_adapter=mock_adapter,
        message_bus=MagicMock(),
        store=None
    )

    msg = Message(sender="user", receiver="triage",type="question", content="传感器数据读取失败")
    result = agent.process(msg)

    assert result == "日志异常"