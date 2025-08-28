from .chat_model import HuggingFaceModel
from .prompts import QA_PROMPT, SUMMARY_PROMPT, REASONING_PROMPT


class QAAgent:
    def __init__(self):
        self.model = HuggingFaceModel(
            "meta-llama/Meta-Llama-3-8B-Instruct",
            quantize=True  
        )

    def answer(self, context: str, question: str) -> str:
        prompt = QA_PROMPT.format(context=context, question=question)
        return self.model.generate(prompt)


class SummarizationAgent:
    def __init__(self):
        self.model = HuggingFaceModel("google/flan-t5-large")

    def summarize(self, text: str) -> str:
        prompt = SUMMARY_PROMPT.format(text=text)
        return self.model.generate(prompt)


class ReasoningAgent:
    def __init__(self):
        self.model = HuggingFaceModel(
            "tiiuae/falcon-7b-instruct",
            quantize=True
        )

    def reason(self, question: str) -> str:
        prompt = REASONING_PROMPT.format(question=question)
        return self.model.generate(prompt)
