import weaviate
from weaviate.classes.config import Property, DataType

class DBManager:
    def __init__(self, url="http://localhost:8080", index_name="PdfChunks"):
        """
        Initialize Weaviate client and ensure schema exists.
        """
        self.client = weaviate.Client(url)
        self.index_name = index_name

        # Check if schema already exists
        if not self.client.schema.exists(self.index_name):
            print(f"Creating schema for {self.index_name}...")
            self.client.schema.create_class({
                "class": self.index_name,
                "properties": [
                    {"name": "text", "dataType": ["text"]},
                    {"name": "pdf_name", "dataType": ["string"]},
                    {"name": "page", "dataType": ["int"]}
                ],
                "vectorizer": "none"  # we supply embeddings manually
            })

    def add_chunk(self, text, embedding, metadata):
        """
        Add a chunk with its embedding + metadata to Weaviate.
        metadata: dict with at least {"pdf_name": str, "page": int}
        """
        obj = {
            "text": text,
            "pdf_name": metadata.get("pdf_name", "unknown"),
            "page": metadata.get("page", -1)
        }
        self.client.data_object.create(
            data_object=obj,
            class_name=self.index_name,
            vector=embedding
        )

    def search(self, query_embedding, k=5):
        """
        Retrieve top-k most similar chunks by vector search.
        Returns: list of dicts (text + metadata)
        """
        result = self.client.query.get(self.index_name, ["text", "pdf_name", "page"]) \
            .with_near_vector({"vector": query_embedding}) \
            .with_limit(k) \
            .do()

        return result.get("data", {}).get("Get", {}).get(self.index_name, [])


if __name__ == "__main__":
    # Example test
    from ingestion.embeddings import EmbeddingsGenerator

    db = DBManager()
    eg = EmbeddingsGenerator()

    # Example: add one chunk
    chunk = "Artificial Intelligence is transforming industries."
    emb = eg.embed(chunk)
    db.add_chunk(chunk, emb, {"pdf_name": "test.pdf", "page": 1})

    # Example: search
    query = "What is AI used for?"
    query_emb = eg.embed(query)
    results = db.search(query_emb, k=2)
    print(results)
