from unittest.mock import MagicMock
from core.message import Message
from agents.doc import DocAgent
from core.knowledge_store import MockStore

def test_doc():
    mock_adapter = MagicMock()
    mock_adapter.chat.return_value = '{"thinking": "查阅配置文档", "answer": "传感器A阈值为100"}'

    mockstore = MockStore()
    mockstore.store("传感器A阈值为100", "配置文档", 1, "配置手册")

    agent = DocAgent(
        model_adapter=mock_adapter,
        store=mockstore
    )

    msg = Message(sender="user", receiver="doc", type="question", content="传感器A阈值是多少")
    result = agent.process(msg)

    assert result["answer"] == "传感器A阈值为100"