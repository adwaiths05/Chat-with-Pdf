from qdrant_client.models import Distance, VectorParams


class DBSchema:
    COLLECTION_NAME = "pdf_chunks"
    VECTOR_SIZE = 768  # depends on embedding model
    DISTANCE = Distance.COSINE

    @staticmethod
    def vector_params():
        return VectorParams(size=DBSchema.VECTOR_SIZE, distance=DBSchema.DISTANCE)
