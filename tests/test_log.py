from unittest.mock import MagicMock
from core.message import Message
from agents.log import LogAgent

def test_log():
    mock_adapter = MagicMock()
    mock_adapter.chat.return_value = '{"thinking": "分析日志", "error_type": "通信中断", "time_pattern": "突发", "impact_scope": "摄像头", "severity": "严重", "suggestion": "重启传感器"}'

    mock_store = MagicMock()
    mock_store.retrieve.return_value = []

    agent = LogAgent(
        model_adapter=mock_adapter,
        store=mock_store
    )

    msg = Message(
        sender="user",
        receiver="log",
        type="analysis",
        content="传感器数据读取失败"
    )

    result = agent.process(msg)

    assert result["error_type"] == "通信中断"
    assert result["severity"] == "严重"
