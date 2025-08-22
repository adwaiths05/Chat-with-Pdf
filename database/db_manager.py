from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
from database.schema import DBSchema


class DBManager:
    def __init__(self, collection_name=DBSchema.COLLECTION_NAME, host="localhost", port=6333):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name

        # Ensure collection exists
        if collection_name not in [c.name for c in self.client.get_collections().collections]:
            print(f"Creating collection: {collection_name}")
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=DBSchema.vector_params()
            )

    def add_chunk(self, text, embedding, metadata):
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
        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=k,
        )
        return [
            {**hit.payload, "score": hit.score}
            for hit in hits
        ]
