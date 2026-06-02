from abc import ABC, abstractmethod
import os
import requests

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

class DifyStore(KnowledgeStore):
    def __init__(self, api_key, dataset_id):
        self.api_key = api_key
        self.dataset_id = dataset_id
        self.base_url = "https://api.dify.ai/v1"
        self.search_method = os.getenv("DIFY_SEARCH_METHOD", "keyword_search")

    def store(self, content, doc_type, doc_id, name):
        pass

    def retrieve(self, query):
        url = f"{self.base_url}/datasets/{self.dataset_id}/retrieve"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "query": query,
            "retrieval_model": {
                "search_method": self.search_method,
                "reranking_enable": False,
                "score_threshold_enabled": False,
                "top_k": 5
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()

            documents = []
            for record in result.get("records", []):
                doc = {
                    "content": record["segment"]["content"],
                    "doc_type": "knowledge_base",
                    "doc_id": record["segment"]["document_id"],
                    "name": record["segment"]["document"]["name"]
                }
                documents.append(doc)

            return documents
        except Exception as e:
            print(f"Dify API 错误: {e}")
            return []
