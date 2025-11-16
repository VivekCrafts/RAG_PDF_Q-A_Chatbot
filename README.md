# RAG API — "Chat With Your Document"
AI/ML Internship Assessment Project  
InnoNexus X JW Infotech

## 🚀 Overview
This project implements a Retrieval-Augmented Generation (RAG) application using FastAPI, FAISS, LangChain, and HuggingFace embeddings.  
The system ingests the **Transformer paper (Attention Is All You Need)**, builds a vector store, and allows users to ask questions through an API.

A bonus **Streamlit UI** is included for interacting with the API.

---

## 📌 Features
- PDF ingestion & text chunking using LangChain
- Embeddings with HuggingFace (e.g., `all-MiniLM-L6-v2`)
- Vector store using **FAISS**
- RAG pipeline using a free LLM API (Gemini/OpenRouter/etc.)
- FastAPI server with one endpoint:  
  **POST /ask** → returns answer + context
- Dockerized backend (FastAPI)
- Bonus Streamlit frontend calling the API

---

## 📁 Directory Structure

```
.
project/
├── main.py
├── app_streamlit.py
├── Dockerfile
├── requirements.txt
├── secreat_key.py
│
├── data/
│   └── Transformer paper.pdf
│
└── README.md

```

---

## 🛠️ Setup & Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/rag-api-transformer.git
cd rag-api-transformer
```

---

## 📦 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🧠 3️⃣ Run the FastAPI Server
```bash
uvicorn app.main:app --reload
```

API will be available at:
```
http://127.0.0.1:8000
```

### Test the API:
```bash
curl -X POST "http://127.0.0.1:8000/ask" \
-H "Content-Type: application/json" \
-d '{"question": "What is self-attention?"}'
```

---

## 🐳 4️⃣ Docker Build & Run

### Build Docker Image
```bash
docker build -t rag-api .
```

### Run Container
```bash
docker run -p 8000:8000 rag-api
```

---

## 🖥️ 5️⃣ Run Streamlit UI (Bonus)

In a new terminal:
```bash
streamlit run ui/app_streamlit.py
```

The UI will:
- Accept user queries
- Call the FastAPI `/ask` endpoint
- Display answer + retrieved context

---

## 🧪 API Endpoint

### **POST /ask**
Request:
```json
{
  "question": "Your question here"
}
```

Response:
```json
{
  "question": "...",
  "answer": "...",
  "context": "Retrieved document chunks..."
}
```

---

## 📘 Evaluation Criteria Checklist

| Requirement | Completed |
|------------|-----------|
| FastAPI RAG API | ✅ |
| FAISS Vector Store | ✅ |
| Embeddings (HuggingFace) | ✅ |
| RAG Chain with LLM | ✅ |
| `/ask` endpoint | ✅ |
| Dockerfile | ✅ |
| Streamlit UI | ✅ |
| Clean README | ✅ |

---
 