# 📘 Chat with PDFs

Chat with multiple PDF documents using LLMs + Weaviate (vector DB).  
This project lets you upload PDFs, process them into embeddings, and then ask natural language questions — with citations and cross-document reasoning.

---

## 🚀 Features

<h1>📘 Chat with PDFs</h1>

Interact with multiple PDF documents using LLMs and Qdrant (vector database). Upload PDFs, process them into embeddings, and ask natural language questions — with citations and cross-document reasoning.

---

## 🚀 Features

- Upload and query multiple PDFs in natural language
- Store embeddings in Qdrant (local, via Docker)
- Hybrid search (semantic + keyword)
- Citations with page numbers and sections
- Modular design: easily extend with agents, summarizers, or different vector DBs

---

## 📂 Project Structure

```
chat-with-pdfs/
│── .env                        # Environment variables
│── requirements.txt            # Base dependencies for backend
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
│   └── schema.py               # Metadata schema (page, section, etc.)
│
├── ingestion/
│   ├── __init__.py
│   ├── pdf_loader.py           # Extracts text from PDFs
│   ├── text_splitter.py        # Splits into chunks
│   ├── embeddings.py           # Generates embeddings (HuggingFace/OpenAI)
│   └── pipeline.py             # Orchestration: load → split → embed → store
│
├── retrieval/
│   ├── __init__.py
│   ├── retriever.py            # Retrieves relevant chunks
│   ├── reranker.py             # (Optional) re-rank results
│   └── hybrid_search.py        # If using keyword+vector
│
├── llm/
│   ├── __init__.py
│   ├── chat_model.py           # Wrapper for GPT/LLaMA etc.
│   ├── prompts.py              # Custom prompts (summaries, compare, explain)
│   └── agents.py               # Specialized agents (summarizer, comparer, reasoner)
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
│   ├── Dockerfile              # Docker container for backend
│   └── entrypoint.py           # Starts app or orchestrates services
│
└── qdrant/
    └── storage/                # Persistent DB storage for Qdrant
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository & Install Requirements

```bash
git clone https://github.com/yourusername/chat-with-pdfs.git
cd chat-with-pdfs
pip install -r requirements.txt
```

### 2. Install & Run Qdrant with Docker

- **Install Docker**
  - Windows/Mac: Download Docker Desktop
  - Linux:
    ```bash
    sudo apt update && sudo apt install docker.io -y
    ```

- **Run Qdrant Container**
  ```bash
  docker run -d -p 6333:6333 \
    -v $(pwd)/qdrant/storage:/qdrant/storage \
    qdrant/qdrant
  ```
  - Access Qdrant at: http://localhost:6333
  - Data persists in `qdrant/storage/` volume

### 3. Configure the Project

Edit `.env` or `config.py` as needed:

```python
DB_TYPE = "qdrant"
QDRANT_URL = "http://localhost:6333"
EMBEDDING_DIM = 1536  # Match your embedding model
```

### 4. Process PDFs

Place your PDFs in `data/uploads/` and run:

```bash
python ingestion/pipeline.py
```

This will:
- Extract text
- Split into chunks
- Generate embeddings
- Store in Qdrant

### 5. Run the UI

- **Gradio:**
  ```bash
  python ui/gradio_app.py
  ```

Access the interface at:
- Gradio: http://localhost:7860
- Streamlit: http://localhost:8501

---

## 🛠 Tech Stack

- **LLM:** Local LLaMA / Hugging Face models
- **Vector DB:** Qdrant (via Docker)
- **Frontend:** Gradio 
- **Embeddings:** SentenceTransformers 
