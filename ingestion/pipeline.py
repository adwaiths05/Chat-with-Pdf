from ingestion.pdf_loader import PDFLoader
from ingestion.text_splitter import TextSplitter
from ingestion.embeddings import EmbeddingsGenerator
from database.db_manager import DBManager
from ingestion.arxiv_client import ArxivMCP

# ----- Existing PDF ingestion -----
def process_pdf(file_path, pdf_name=None):
    loader = PDFLoader(file_path)
    splitter = TextSplitter()
    embedder = EmbeddingsGenerator()
    db = DBManager()

    text = loader.load_text()
    chunks = splitter.split(text)
    embeddings = embedder.embed_batch(chunks)

    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        db.add_chunk(chunk, emb, {"pdf_name": pdf_name or file_path, "page": i})

    print(f"✅ Stored {len(chunks)} chunks from {file_path} into DB")

def ingest_pdf(file_path, pdf_name=None):
    process_pdf(file_path, pdf_name)

# ----- New ArXiv ingestion -----
def ingest_arxiv_paper(title: str):
    arxiv = ArxivMCP()
    embedder = EmbeddingsGenerator()
    splitter = TextSplitter()
    db = DBManager()

    paper_id, text = arxiv.fetch_paper(title)
    chunks = splitter.split(text)
    embeddings = embedder.embed_batch(chunks)

    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        db.add_chunk(chunk, emb, {"paper_id": paper_id, "page": i})

    print(f"✅ Stored {len(chunks)} chunks from '{title}' into DB")

# ----- Optional: unified interface -----
def ingest(file_path_or_title: str, source_type="pdf"):
    if source_type == "pdf":
        ingest_pdf(file_path_or_title)
    elif source_type == "arxiv":
        ingest_arxiv_paper(file_path_or_title)
    else:
        raise ValueError(f"Unknown source_type: {source_type}")

if __name__ == "__main__":
    # Example usage:
    process_pdf("sample.pdf", pdf_name="sample.pdf")
    # ingest_arxiv_paper("Quantum Embeddings in NLP")
