from sentence_transformers import SentenceTransformer

class EmbeddingsGenerator:
    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5"):
        print(f"🔹 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str):
        """Generate a single embedding"""
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: list[str]):
        """Generate embeddings for multiple texts"""
        return self.model.encode(texts).tolist()
