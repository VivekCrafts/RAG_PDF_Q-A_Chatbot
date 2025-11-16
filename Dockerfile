# =============================
#  FastAPI RAG Dockerfile
# =============================
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# -----------------------------
# Install system dependencies
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Install FAISS CPU (important)
# -----------------------------
RUN pip install --no-cache-dir faiss-cpu

# -----------------------------
# Copy requirements & install
# -----------------------------
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy the whole project
# -----------------------------
COPY . .

# Make sure data directory exists
RUN mkdir -p /app/data

# -----------------------------
# Expose FastAPI port
# -----------------------------
EXPOSE 8000

# -----------------------------
# Environment variables (optional)
# -----------------------------
ENV PDF_PATH="data/Transformer paper.pdf"
ENV CHUNK_SIZE=800
ENV CHUNK_OVERLAP=150
ENV TOP_K=3

# IMPORTANT: Provide API KEY at runtime instead of hardcoding
ENV GOOGLE_API_KEY=""

# -----------------------------
# Start FastAPI
# -----------------------------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
