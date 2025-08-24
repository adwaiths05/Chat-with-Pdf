# config.py

# Qdrant settings (local Docker by default)
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
QDRANT_COLLECTION = "pdf_chunks"

# Embedding model
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

# LLM models (change to smaller ones if running locally!)
LLM_QA_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
LLM_SUMMARY_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
LLM_REASONING_MODEL = "openai-community/gpt-4o-mini-oss"
