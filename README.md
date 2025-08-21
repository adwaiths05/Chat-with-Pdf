# 📘 Chat with PDFs

Chat with multiple PDF documents using LLMs + Weaviate (vector DB).  
This project lets you upload PDFs, process them into embeddings, and then ask natural language questions — with citations and cross-document reasoning.

---

## 🚀 Features

- Upload multiple PDFs and query them in natural language
- Store embeddings in Weaviate (local or cloud)
- Hybrid search (semantic + keyword)
- Citations with page numbers + sections
- Modular design → easy to extend with agents, summarizers, or different vector DBs

---

## 📂 Project Structure

```
chat-with-pdfs/
│── app.py                  # Main entry point (UI or API)
│── config.py               # Config (DB settings, API keys)
│── requirements.txt        # Dependencies
│── README.md               # Documentation
│
├── data/                   # Raw and processed files
│   ├── uploads/            # User-uploaded PDFs
│   ├── processed/          # Extracted text/chunks
│
├── database/               # Vector DB logic
│   ├── db_manager.py
│   ├── schema.py
│
├── ingestion/              # PDF → text → chunks → embeddings
│   ├── pdf_loader.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── pipeline.py
│
├── retrieval/              # Query pipeline
│   ├── retriever.py
│   ├── hybrid_search.py
│
├── llm/                    # LLM logic
│   ├── chat_model.py
│   ├── prompts.py
│
├── ui/                     # Frontend
│   ├── streamlit_app.py
│   ├── gradio_app.py
│
└── tests/                  # Unit tests
```

---

## ⚙️ Setup Instructions

### 1. Clone Repo & Install Requirements

```sh
git clone https://github.com/yourusername/chat-with-pdfs.git
cd chat-with-pdfs
pip install -r requirements.txt
```

### 2. Install & Run Weaviate with Docker

**Install Docker**

- Download Docker Desktop (Windows/Mac)
- Linux:
  ```sh
  sudo apt update && sudo apt install docker.io -y
  ```

**Run Weaviate Container**

```sh
docker run -d -p 8080:8080 \
    -v weaviate_data:/var/lib/weaviate \
    semitechnologies/weaviate \
    --host 0.0.0.0 \
    --port 8080 \
    --modules-text2vec-openai
```

Access: [http://localhost:8080/v1/graphql](http://localhost:8080/v1/graphql)  
This persists data in a Docker volume `weaviate_data`.

### 3. Configure Project

Edit `config.py`:

```python
DB_TYPE = "weaviate"
WEAVIATE_URL = "http://localhost:8080"
WEAVIATE_API_KEY = None  # Not needed for local
EMBEDDING_DIM = 1536     # Match your embedding model
```

### 4. Process PDFs

Put your PDFs into `data/uploads/` and run:

```sh
python ingestion/pipeline.py
```

This will:

- Extract text
- Split into chunks
- Generate embeddings
- Store in Weaviate

### 5. Query the PDFs

Run the UI (Streamlit example):

```sh
streamlit run ui/streamlit_app.py
```

Now you can upload/query PDFs interactively 🎉

---

## 🛠 Tech Stack

- **LLM:** OpenAI GPT / Local LLaMA
- **Vector DB:** Weaviate (local Docker or cloud)
- **Frontend:** Streamlit / Gradio
- **Embeddings:** OpenAI or SentenceTransformers
