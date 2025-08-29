from .chat_model import HuggingFaceModel
from .prompts import QA_PROMPT, SUMMARY_PROMPT, REASONING_PROMPT
from ingestion.pipeline import ingest_arxiv_paper
from retrieval.retriever import Retriever  # assuming this queries Qdrant


class QAAgent:
    def __init__(self):
        self.model = HuggingFaceModel(
            "meta-llama/Meta-Llama-3-8B-Instruct",
            quantize=True
        )
        self.retriever = Retriever()

    def answer(self, context: str, question: str, arxiv_title: str = None) -> str:
        # 1️⃣ If an ArXiv paper is mentioned and not in DB, ingest it
        if arxiv_title:
            if not self.retriever.has_paper(arxiv_title):
                ingest_arxiv_paper(arxiv_title)
            context = self.retriever.get_context_for_paper(arxiv_title)

        prompt = QA_PROMPT.format(context=context, question=question)
        return self.model.generate(prompt)


class SummarizationAgent:
    def __init__(self):
        self.model = HuggingFaceModel("google/flan-t5-large")
        self.retriever = Retriever()

    def summarize(self, text: str = None, arxiv_title: str = None) -> str:
        # Dynamically fetch content if ArXiv title provided
        if arxiv_title:
            if not self.retriever.has_paper(arxiv_title):
                ingest_arxiv_paper(arxiv_title)
            text = self.retriever.get_context_for_paper(arxiv_title)

        prompt = SUMMARY_PROMPT.format(text=text)
        return self.model.generate(prompt)


class ReasoningAgent:
    def __init__(self):
        self.model = HuggingFaceModel(
            "tiiuae/falcon-7b-instruct",
            quantize=True
        )
        self.retriever = Retriever()

    def reason(self, question: str, arxiv_title: str = None) -> str:
        # Optionally fetch new ArXiv content for reasoning
        context = ""
        if arxiv_title:
            if not self.retriever.has_paper(arxiv_title):
                ingest_arxiv_paper(arxiv_title)
            context = self.retriever.get_context_for_paper(arxiv_title)
