from sentence_transformers import SentenceTransformer


class EmbeddingsGenerator:
    def __init__(self, model_name="BAAI/bge-base-en-v1.5"):
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def embed(self, text):
        """
        Returns a single embedding vector.
        """
        return self.model.encode(text).tolist()

    def embed_batch(self, texts):
        """
        Returns embeddings for a list of texts.
        """
        return self.model.encode(texts).tolist()
