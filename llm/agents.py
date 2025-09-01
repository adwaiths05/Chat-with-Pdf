from .chat_model import HuggingFaceModel
from .prompts import QA_PROMPT, SUMMARY_PROMPT, REASONING_PROMPT
from ingestion.pipeline import ingest_arxiv_paper
from retrieval.retriever import Retriever  # assuming this queries Qdrant


class QAAgent:
    def __init__(self):
        # Use a lightweight model (T5 works well on CPU)
        self.model = HuggingFaceModel(
            "google/flan-t5-base",
            quantize=False   # force off for CPU safety
        )
        self.retriever = Retriever()

    def answer(self, context: str, question: str, arxiv_title: str = None) -> str:
        if arxiv_title:
            if not self.retriever.has_paper(arxiv_title):
                ingest_arxiv_paper(arxiv_title)
            context = self.retriever.get_context_for_paper(arxiv_title)

        prompt = QA_PROMPT.format(context=context, question=question)
        return self.model.generate(prompt)


class SummarizationAgent:
    def __init__(self):
        # T5-large can still run on CPU, slower though
        self.model = HuggingFaceModel(
            "google/flan-t5-base",
            quantize=False
        )
        self.retriever = Retriever()

    def summarize(self, text: str = None, arxiv_title: str = None) -> str:
        if arxiv_title:
            if not self.retriever.has_paper(arxiv_title):
                ingest_arxiv_paper(arxiv_title)
            text = self.retriever.get_context_for_paper(arxiv_title)

        prompt = SUMMARY_PROMPT.format(text=text)
        return self.model.generate(prompt)


class ReasoningAgent:
    def __init__(self):
        # Falcon is heavy, only use quantize if GPU is available
        self.model = HuggingFaceModel(
            "tiiuae/falcon-rw-1b",
            quantize=True
        )
        self.retriever = Retriever()

    def reason(self, question: str, arxiv_title: str = None) -> str:
        context = ""
        if arxiv_title:
            if not self.retriever.has_paper(arxiv_title):
                ingest_arxiv_paper(arxiv_title)
            context = self.retriever.get_context_for_paper(arxiv_title)

        prompt = REASONING_PROMPT.format(context=context, question=question)
        return self.model.generate(prompt)
