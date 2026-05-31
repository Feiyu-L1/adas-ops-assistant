from unittest.mock import MagicMock
from core.message import Message
from agents.log import LogAgent

def test_log():
    mock_adapter = MagicMock()
    mock_adapter.chat.return_value = "错误类型：通信中断"

    agent = LogAgent(
        model_adapter=mock_adapter,
        message_bus=MagicMock(),
        store=None
    )

    msg = Message(
        sender="user",
        receiver="log",
        type="analysis",
        content="传感器数据读取失败"
    )

    result = agent.process(msg)

    assert result =="错误类型：通信中断"
