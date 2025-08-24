from ingestion.pdf_loader import PDFLoader
from ingestion.text_splitter import TextSplitter
from ingestion.embeddings import EmbeddingsGenerator
from database.db_manager import DBManager


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

    print(f" Stored {len(chunks)} chunks from {file_path} into DB")

def ingest_pdf(file_path, pdf_name=None):
    process_pdf(file_path, pdf_name)

if __name__ == "__main__":
    process_pdf("sample.pdf", pdf_name="sample.pdf")
