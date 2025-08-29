from database.db_manager import DBManager
from ingestion.embeddings import EmbeddingsGenerator


class Retriever:
    def __init__(self, collection_name="pdf_chunks"):
        self.db = DBManager(collection_name=collection_name)
        self.embedder = EmbeddingsGenerator()

    # ------------------------
    # Semantic search
    # ------------------------
    def retrieve(self, query: str, top_k: int = 5):
        query_vector = self.embedder.embed(query)
        results = self.db.search(query_vector, k=top_k)

        context = "\n".join([f"{r['text']} (Page {r['page']})" for r in results])
        return context, results

    # ------------------------
    # Check if paper is in DB
    # ------------------------
    def has_paper(self, paper_id_or_title: str) -> bool:
        # Check DB metadata for pdf_name or paper_id
        results = self.db.filter({"pdf_name": paper_id_or_title})
        if not results:
            results = self.db.filter({"paper_id": paper_id_or_title})
        return len(results) > 0

    # ------------------------
    # Get full context for a paper
    # ------------------------
    def get_context_for_paper(self, paper_id_or_title: str) -> str:
        results = self.db.filter({"pdf_name": paper_id_or_title})
        if not results:
            results = self.db.filter({"paper_id": paper_id_or_title})

        # Sort by page for coherent context
        results = sorted(results, key=lambda r: r["page"])
        context = "\n".join([r["text"] for r in results])
        return context
