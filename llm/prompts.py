# Prompt for Q&A with citations
QA_PROMPT = """
You are a research assistant. Answer the question using ONLY the provided context.
Do not invent any information. Include citations in this format: (Document Name, Page Number).
Provide the answer clearly and concisely.

Context:
{context}

Question:
{question}

Answer (with citations):
"""

# Prompt for summarization
SUMMARY_PROMPT = """
You are a summarization assistant. Summarize the following text clearly and concisely.
Highlight the main points, key arguments, and important data.
If the text has sections, summarize each section separately.

Text:
{text}

Summary:
"""

# Prompt for reasoning / clarification
REASONING_PROMPT = """
You are an expert reasoning agent. 
Break the question into steps and reason through each one carefully.
Identify any assumptions or missing information.
Finally, provide a clear answer based on the reasoning.

Question:
{question}

Step-by-step reasoning and final answer:

"""
