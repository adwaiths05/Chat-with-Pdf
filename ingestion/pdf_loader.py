import os
from PyPDF2 import PdfReader


class PDFLoader:
    def __init__(self, folder_path="data/uploads"):
        self.folder_path = folder_path

    def load_pdfs(self):
        """Load all PDFs in the folder and return as dict: {filename: text}"""
        pdf_texts = {}
        for file in os.listdir(self.folder_path):
            if file.endswith(".pdf"):
                path = os.path.join(self.folder_path, file)
                text = self._extract_text(path)
                pdf_texts[file] = text
        return pdf_texts

    def _extract_text(self, pdf_path):
        """Extract text from a single PDF file"""
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""  # handle None
        return text.strip()


if __name__ == "__main__":
    loader = PDFLoader()
    docs = loader.load_pdfs()
    for name, text in docs.items():
        print(f"--- {name} ---")
        print(text[:500])  # preview first 500 chars
