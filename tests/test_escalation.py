from unittest.mock import MagicMock
from core.message import Message
from agents.escalation import EscalationAgent

def test_escalation_process():
    mock_adapater = MagicMock()
    mock_adapater.chat.return_value = "需要升级"

    agent = EscalationAgent(
        model_adapter=mock_adapater,
        message_bus=MagicMock(),
        store=None
    )

    msg = Message(sender="response", receiver="escalation", type="report", content="严重程度：严重")
    result = agent.process(msg)

    assert result == "需要升级"
