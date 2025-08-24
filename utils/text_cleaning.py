import re

def clean_text(text: str) -> str:
    """Basic cleaning: remove extra spaces, line breaks, weird chars"""
    text = re.sub(r"\s+", " ", text)   # collapse spaces
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # remove non-ASCII
    return text.strip()

def preprocess_chunks(chunks: list[str]) -> list[str]:
    """Apply cleaning to list of chunks"""
    return [clean_text(chunk) for chunk in chunks]
