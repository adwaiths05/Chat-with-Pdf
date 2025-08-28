# 📘 Chat with PDFs 
---

## 🚀 Features

Interact with multiple PDF documents and directly fetch papers from sources like ArXiv using LLMs and Qdrant (vector database).

- Upload PDFs or fetch LaTeX content from ArXiv
- Parse LaTeX to text, ignoring equations and section headers
- Store embeddings in Qdrant for semantic search
- Ask natural language questions with context-aware reasoning
- Modular agents: Q&A, Summarization, Reasoning
- Hybrid search (semantic + keyword)
- Citations with page numbers and sections for PDFs

---

## 📂 Project Structure

```
chat-with-pdfs/
│── .env                        # Environment variables
│── .gitignore
│── config.py
│── LICENSE
│── requirements.txt
│── docker-compose.yml          # Orchestrates backend, UI, DB
│── README.md
│
├── data/
│   ├── uploads/                # User-uploaded PDFs
│   └── processed/              # Extracted & chunked text
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py           # Connects to Qdrant
│   └── schema.py               # Metadata schema
│
├── ingestion/
│   ├── __init__.py
│   ├── pdf_loader.py           # Extracts text from PDFs
│   ├── latex_parser.py         # Parses LaTeX to plain text
│   ├── text_splitter.py        # Splits text into chunks
│   ├── embeddings.py           # Generates embeddings
│   ├── arxiv_client.py         # Fetches LaTeX source from ArXiv
│   └── pipeline.py             # Orchestrates load → parse → split → embed → store
│
├── retrieval/
│   ├── __init__.py
│   ├── retriever.py
│   └── hybrid_search.py
│
├── llm/
│   ├── __init__.py
│   ├── chat_model.py           # HuggingFace LLM wrapper
│   ├── prompts.py
│   └── agents.py               # Q&A, Summarizer, Reasoning agents
│
├── utils/
│   ├── __init__.py
│   ├── logging.py
│   ├── pdf_utils.py
│   └── text_cleaning.py
│
├── ui/
│   ├── streamlit_app.py
│   ├── gradio_app.py
│   └── react_frontend/         # Optional full React UI
│
├── backend/
│   ├── Dockerfile
│   └── entrypoint.py
│
└── qdrant/
    └── storage/                # Persistent DB storage for Qdrant
```

---

## ⚙️ Setup Instructions

1. Clone the Repository

```bash
git clone https://github.com/yourusername/chat-with-pdfs.git
cd chat-with-pdfs
```

2. Install Requirements (optional if using Docker)

```bash
pip install -r requirements.txt
```

3. Install & Run Qdrant with Docker

- Install Docker
  - Windows/Mac: Docker Desktop
  - Linux:
    ```bash
    sudo apt update && sudo apt install docker.io -y
    ```

- Run Qdrant Container
  ```bash
  docker run -d -p 6333:6333 \
    -v $(pwd)/qdrant/storage:/qdrant/storage \
    qdrant/qdrant
  ```
  - Access Qdrant: http://localhost:6333

4. Configure Project

Edit .env or config.py:

```python
DB_TYPE = "qdrant"
QDRANT_URL = "http://localhost:6333"
EMBEDDING_DIM = 1536   # Matches embedding model
```

5. Process PDFs or Fetch ArXiv Papers

- For PDFs:
  ```bash
  python ingestion/pipeline.py --source pdf --file data/uploads/sample.pdf
  ```
- For ArXiv papers:
  ```bash
  python ingestion/pipeline.py --source arxiv --arxiv_id 2307.12345
  ```

This will:

- Fetch LaTeX source (if ArXiv)
- Parse to text, excluding equations
- Split into chunks
- Generate embeddings
- Store in Qdrant

6. Run the UI

- Gradio:
  ```bash
  python ui/gradio_app.py
  ```
  Access at http://localhost:7860
- Streamlit:
  ```bash
  streamlit run ui/streamlit_app.py
  ```
  Access at http://localhost:8501

---

##  Tech Stack

- LLM: Local HuggingFace models (e.g., LLaMA, Falcon, Flan-T5)
- Vector DB: Qdrant (semantic search & storage)
- Frontend: Gradio / Streamlit
- Embeddings: SentenceTransformers
- PDF Parsing: PyMuPDF, pdfplumber
- ArXiv Client: Fetch LaTeX source for embedding without downloading PDFs

---

##  Notes

- Embeddings do not include equations.
- LaTeX parsing removes section headers to focus on content.
- Qdrant stores all vectors permanently, enabling semantic search across papers over time.
- Modular design: add more sources like Springer, Google Scholar, etc. in the future.
