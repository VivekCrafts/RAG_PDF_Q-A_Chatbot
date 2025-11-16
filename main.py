# main.py
import os
import textwrap
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import numpy as np
import faiss
import google.generativeai as genai
from secreat_key import GOOGLE_API_KEY  # must contain your key

PDF_PATH = "data/Transformer paper.pdf"  # <-- your PDF path
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 3

app = FastAPI(title="Simple RAG - Transformer Paper")

class AskRequest(BaseModel):
    question: str

# -------------------------------
# Root endpoint
# -------------------------------
@app.get("/")
def root():
    return {"message": "FastAPI server is running! Use /ask endpoint to query your PDF."}

# -------------------------------
# Load PDF
# -------------------------------
def load_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            texts.append(t)
    return "\n\n".join(texts)

# -------------------------------
# Chunk text
# -------------------------------
def chunk_text(text: str, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    i = 0
    L = len(text)
    while i < L:
        end = min(i + size, L)
        chunks.append(text[i:end].strip())
        if end == L:
            break
        i = max(0, end - overlap)
    return chunks

# -------------------------------
# Build embeddings + FAISS
# -------------------------------
def build_index(local_chunks: List[str]):
    global embedder, index
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    embs = embedder.encode(local_chunks, convert_to_numpy=True).astype("float32")
    dim = embs.shape[1]
    idx = faiss.IndexFlatL2(dim)
    idx.add(embs)
    index = idx

# -------------------------------
# Retrieve top K chunks
# -------------------------------
def retrieve(query: str, k=TOP_K):
    q = embedder.encode([query], convert_to_numpy=True).astype("float32")
    D, I = index.search(q, k)
    return [chunks[i] for i in I[0]]

# -------------------------------
# Build prompt
# -------------------------------
def make_prompt(context_chunks: List[str], question: str) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    return textwrap.dedent(f"""
    Answer the question using ONLY the context provided.
    
    CONTEXT:
    {context}

    QUESTION:
    {question}

    If the answer is not in the context, say:
    "I couldn't find a direct answer in the provided context."
    """).strip()

# -------------------------------
# Call Gemini (fixed for your SDK)
# -------------------------------
def call_gemini(prompt: str):
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is missing in secreat_key.py")

    # Configure API key
    genai.configure(api_key=GOOGLE_API_KEY)

    # Use GenerativeModel (correct for your installed package)
    model = genai.GenerativeModel("gemini-2.5-flash")  # valid model
    resp = model.generate_content(prompt)

    # Extract text safely
    try:
        return resp.text
    except AttributeError:
        return resp["candidates"][0]["content"]

# -------------------------------
# Startup: load PDF, chunk, build index
# -------------------------------
@app.on_event("startup")
def startup():
    global chunks
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found at: {PDF_PATH}")

    text = load_text_from_pdf(PDF_PATH)
    chunks = chunk_text(text)
    build_index(chunks)
    print(f"[INFO] Loaded PDF and built FAISS index with {len(chunks)} chunks.")

# -------------------------------
# /ask endpoint
# -------------------------------
@app.post("/ask")
def ask(req: AskRequest):
    q = req.question.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Empty question")

    retrieved = retrieve(q)
    prompt = make_prompt(retrieved, q)

    try:
        answer = call_gemini(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "question": q,
        "answer": answer,
        
    }
