from core.knowledge_store import MockStore

def test_store_and_retrieve():
    mstore = MockStore()
    mstore.store("高级传感器", "传感器文档", 1, "cgq说明书")
    assert len(mstore.documents) == 1
    assert len(mstore.retrieve("传感器")) == 1
    assert len(mstore.retrieve("发动机")) == 0