from database.db_manager import DBManager
from ingestion.embeddings import EmbeddingsGenerator


class Retriever:
    def __init__(self, collection_name="pdf_chunks"):
        self.db = DBManager(collection_name=collection_name)
        self.embedder = EmbeddingsGenerator()

    def retrieve(self, query: str, top_k: int = 5):
        query_vector = self.embedder.embed(query)
        results = self.db.search(query_vector, k=top_k)

        # Combine chunks as context
        context = "\n".join([f"{r['text']} (Page {r['page']})" for r in results])
        return context, results
