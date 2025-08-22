from .chat_model import HuggingFaceModel
from .prompts import QA_PROMPT, SUMMARY_PROMPT, REASONING_PROMPT

class QAAgent:
    def __init__(self):
        # Q&A Agent -> LLaMA-3 8B Instruct
        self.model = HuggingFaceModel("meta-llama/Meta-Llama-3-8B-Instruct")

    def answer(self, context: str, question: str) -> str:
        prompt = QA_PROMPT.format(context=context, question=question)
        return self.model.generate(prompt)


class SummarizationAgent:
    def __init__(self):
        # Summarization Agent -> LLaMA-3 70B Instruct
        self.model = HuggingFaceModel("meta-llama/Meta-Llama-3-70B-Instruct")

    def summarize(self, text: str) -> str:
        prompt = SUMMARY_PROMPT.format(text=text)
        return self.model.generate(prompt)


class ReasoningAgent:
    def __init__(self):
        # Reasoning Agent -> GPT-4o Mini OSS
        self.model = HuggingFaceModel("openai-community/gpt-4o-mini-oss")

    def reason(self, question: str) -> str:
        prompt = REASONING_PROMPT.format(question=question)
        return self.model.generate(prompt)
