from abc import ABC, abstractmethod

class KnowledgeStore(ABC):
    @abstractmethod
    def store(self, content, doc_type, doc_id, name):
        pass
    @abstractmethod    
    def retrieve(self, query):
        pass

class MockStore(KnowledgeStore):
    def __init__(self):
        self.documents = []     # An empty list, used to store documents

    def store(self, content, doc_type, doc_id, name):
        doc = {
            "content": content,
            "doc_type": doc_type,
            "doc_id": doc_id,
            "name": name
        }
        self.documents.append(doc)

    def retrieve(self, query):
        results = []
        for doc in self.documents:
            if query in doc["content"]:
                results.append(doc)
        return results

