from sentence_transformers import SentenceTransformer

class EmbeddingsGenerator:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def embed(self, text):
        """Generate embedding vector for a single text"""
        return self.model.encode(text).tolist()

    def embed_batch(self, texts):
        """Generate embeddings for a list of texts"""
        return self.model.encode(texts, convert_to_numpy=False).tolist()


if __name__ == "__main__":
    eg = EmbeddingsGenerator()
    emb = eg.embed("Hello world, this is a test embedding.")
    print(len(emb), emb[:5])  # show dimension + first 5 numbers
