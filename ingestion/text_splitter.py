import re

class TextSplitter:
    def __init__(self, chunk_size=500, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text):
        """Split long text into overlapping chunks"""
        text = re.sub(r"\s+", " ", text)  # clean whitespace
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunks.append(text[start:end])
            start += self.chunk_size - self.overlap
        return chunks


if __name__ == "__main__":
    sample_text = "This is a test sentence. " * 50
    splitter = TextSplitter()
    chunks = splitter.split_text(sample_text)
    for c in chunks[:3]:
        print(c)
