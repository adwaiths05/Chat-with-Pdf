from pypdf import PdfReader


class PDFLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_text(self):
        """
        Extract raw text from a PDF.
        """
        reader = PdfReader(self.file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
