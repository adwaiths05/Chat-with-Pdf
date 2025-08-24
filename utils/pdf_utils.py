import fitz  # PyMuPDF
import pdfplumber

def extract_text_pymupdf(file_path: str) -> list[str]:
    """Extract text per page using PyMuPDF"""
    doc = fitz.open(file_path)
    texts = [page.get_text("text") for page in doc]
    doc.close()
    return texts

def extract_text_pdfplumber(file_path: str) -> list[str]:
    """Extract text per page using pdfplumber"""
    texts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            texts.append(page.extract_text() or "")
    return texts

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks for embeddings"""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
