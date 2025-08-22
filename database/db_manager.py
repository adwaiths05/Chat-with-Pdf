from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid


class DBManager:
    def __init__(self, collection_name="pdf_chunks", host="localhost", port=6333):
        """
        Initialize Qdrant client and ensure collection exists.
        """
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name

        # Create collection if it doesn’t exist
        if collection_name not in [c.name for c in self.client.get_collections().collections]:
            print(f"Creating collection: {collection_name}")
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE)  # assuming 768-dim embeddings
            )

    def add_chunk(self, text, embedding, metadata):
        """
        Add one chunk with its embedding + metadata to Qdrant.
        """
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "text": text,
                "pdf_name": metadata.get("pdf_name", "unknown"),
                "page": metadata.get("page", -1),
            },
        )
        self.client.upsert(collection_name=self.collection_name, points=[point])

    def search(self, query_embedding, k=5):
        """
        Retrieve top-k most similar chunks by vector search.
        Returns: list of dicts with text + metadata.
        """
        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=k,
        )
        results = []
        for hit in hits:
            payload = hit.payload
            payload["score"] = hit.score
            results.append(payload)
        return results


if __name__ == "__main__":
    # Example test
    from ingestion.embeddings import EmbeddingsGenerator

    db = DBManager()
    eg = EmbeddingsGenerator()

    chunk = "Artificial Intelligence is transforming industries."
    emb = eg.embed(chunk)
    db.add_chunk(chunk, emb, {"pdf_name": "test.pdf", "page": 1})

    query = "What is AI used for?"
    query_emb = eg.embed(query)
    results = db.search(query_emb, k=2)
    print(results)
