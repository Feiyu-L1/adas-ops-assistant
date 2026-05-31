from unittest.mock import MagicMock
from core.message import Message
from agents.response import ResponseAgent

def test_response_process():
    mock_adapter = MagicMock()
    mock_adapter.chat.return_value = "## 故障报告\n- 问题描述：传感器通信中断"

    agent = ResponseAgent(
        model_adapter=mock_adapter,
        message_bus=MagicMock(),
        store=None
    )

    msg = Message(sender="log", receiver="response", type="report",content="错误类型：通信中断，严重程度：中等")
    result = agent.process(msg)

    assert result == "## 故障报告\n- 问题描述：传感器通信中断"