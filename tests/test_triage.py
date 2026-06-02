from unittest.mock import MagicMock
from core.message import Message
from agents.triage import TriageAgent

def test_triage_process():
    mock_adapter = MagicMock()
    mock_adapter.chat.return_value = '{"thinking": "用户描述了传感器报错", "intent": "日志异常"}'

    agent = TriageAgent(
        model_adapter=mock_adapter,
        store=None
    )

    msg = Message(sender="user", receiver="triage", type="question", content="传感器数据读取失败")
    result = agent.process(msg)

    assert result["intent"] == "日志异常"