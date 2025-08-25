# 📘 Chat with PDFs

🚀 Features

Interact with multiple PDF documents using LLMs and Qdrant (vector database). Upload PDFs, process them into embeddings, and ask natural language questions — with citations and cross-document reasoning.

- Upload and query multiple PDFs in natural language
- Store embeddings in Qdrant (local, via Docker)
- Hybrid search (semantic + keyword)
- Citations with page numbers and sections
- Modular design: extend with summarizers, agents, or a different vector DB

---

📂 Project Structure

```
chat-with-pdfs/
│── .env                        # Environment variables
│── requirements.txt            # Base dependencies
│── docker-compose.yml          # (optional) orchestrates backend + Qdrant
│── README.md
│
├── backend/
│   ├── Dockerfile              # Backend container
│   └── entrypoint.py           # Starts FastAPI + Gradio app
│
├── data/
│   ├── uploads/                # User-uploaded PDFs
│   └── processed/              # Extracted & chunked text
│
├── ingestion/                  # PDF → text → embeddings pipeline
│   ├── pdf_loader.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   └── pipeline.py
│
├── retrieval/                  # Search & retrieval
│   ├── retriever.py
│   └── hybrid_search.py
│
├── llm/                        # LLM integration
│   ├── chat_model.py
│   └── prompts.py
│
├── ui/
│   ├── gradio_app.py
│   └── streamlit_app.py
│
└── qdrant/
    └── storage/                # Persistent DB storage
```

---

⚙️ Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/yourusername/chat-with-pdfs.git
cd chat-with-pdfs
```

2. Start Qdrant (Vector DB)

Run Qdrant container:

```bash
docker run -d -p 6333:6333 \
  -v $(pwd)/qdrant/storage:/qdrant/storage \
  qdrant/qdrant
```

Qdrant Dashboard → http://localhost:6333

Data persists in qdrant/storage/

3. Build the backend image

```bash
docker build -t chat-pdfs-backend -f backend/Dockerfile .
```

This will:

- Install dependencies from requirements.txt
- Copy project code into /app inside the container
- Set up Gradio server at port 7860

4. Run the backend

```bash
docker run -p 7860:7860 chat-pdfs-backend
```

Now access the app at:
👉 http://localhost:7860

---

📚 Usage

**Process PDFs**

Place PDFs in `data/uploads/` then run:

```bash
python ingestion/pipeline.py
```

This will:

- Extract text
- Split into chunks
- Generate embeddings
- Store them in Qdrant

**Query PDFs**

- Via Gradio UI → http://localhost:7860
- Or via Streamlit (optional):

```bash
python ui/streamlit_app.py
```

---

🛑 Stopping

**Stop backend:**

```bash
docker ps   # find container id
docker stop <container_id>
```

**Stop Qdrant:**

```bash
docker stop $(docker ps -q --filter ancestor=qdrant/qdrant)
```

Closing Docker Desktop also stops all containers.

---

🛠 Tech Stack

- LLM: HuggingFace / local models
- Vector DB: Qdrant (Dockerized)
- Backend: FastAPI + Gradio
- Embeddings: SentenceTransformers
- UI: Gradio + Streamlit
