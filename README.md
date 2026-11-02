# 🌿 MindCare AI — Empathetic Mental Wellness Chatbot (MVP 1.0)

> **MindCare AI** is an AI-powered mental wellness conversational companion built with **FastAPI**, **React (TypeScript)**, **Retrieval-Augmented Generation (RAG)** via **Qdrant** and **Sentence-Transformers (`all-MiniLM-L6-v2`)**, persistent **SQL conversational memory**, and a **dedicated crisis safety screening layer**.

---

## 🌟 Key Capabilities

1. **RAG-Grounded Wellness Knowledge:**
   - Curated knowledge base covering **Cognitive Behavioral Therapy (CBT)**, **Dialectical Behavior Therapy (DBT)**, **Somatic Grounding (5-4-3-2-1)**, **Sleep Hygiene**, **Circadian Rhythm**, and **Burnout Prevention**.
   - Embeddings powered by `sentence-transformers/all-MiniLM-L6-v2` with cosine distance indexing in **Qdrant**.
   - Source citations surfaced on each assistant response with relevance scoring.

2. **Mandatory Crisis Safety Screening:**
   - Independent safety guardrail executed **before** any RAG or LLM generation.
   - Detects explicit suicide threats, acute self-harm, and immediate danger.
   - Bypasses ordinary response generation to provide empathetic crisis intervention and regional emergency hotlines:
     - 🇮🇳 **India:** Emergency **112**, Tele-MANAS **14416 / 1800-891-4416**, Vandrevala Foundation **+91 9999 666 555**
     - 🇺🇸 🇨🇦 **US & Canada:** Suicide & Crisis Lifeline **988**, Crisis Text Line (Text **HOME to 741741**)
     - 🇬🇧 **UK:** Emergency **999**, Samaritans **116 123**
     - 🌐 **International:** [Befrienders Worldwide](https://www.befrienders.org)

3. **Persistent SQL Multi-Turn Memory:**
   - Relational database schema for `users`, `sessions`, and `messages`.
   - Maintains context across **30 conversational turns (60 messages)** with automatic token budgeting.
   - Enforces strict user authorization: users can never access or query other users' sessions.

4. **Modern Calming Interface:**
   - Built with React, TypeScript, and Tailwind CSS using a calm wellness palette (`#557C78`, `#A9C4B8`, `#F7F9F7`).
   - Interactive conversation management: New chat, rename, delete, and session indicators.
   - Grounded citations viewer modal and upload interface for PDFs, TXT, and Markdown files.

---

## 🏛️ System Architecture

```text
User Message
    │
    ▼
Frontend (React 18 + TypeScript + Tailwind)
    │
    ▼
FastAPI Backend
    │
    ▼
Authentication & JWT Validation
    │
    ▼
[Safety Screening Layer] ──(Crisis Detected?)──► Emergency Helplines & Safety Guidance (112 / 14416 / 988)
    │ (Safe)
    ▼
Conversation Memory Retrieval (PostgreSQL / SQLite, 30 turns)
    │
    ▼
RAG Query Vector Embedding (all-MiniLM-L6-v2)
    │
    ▼
Vector Database (Qdrant)
    │
    ▼
Relevant Knowledge Chunks (Top-K = 5)
    │
    ▼
LLM Empathetic Response Generation (Gemini / OpenAI / Grounded Fallback)
    │
    ▼
Return Response with Sources + Save to SQL Database
```

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- (Optional) Docker & Docker Compose

---

### Option 1: Local Development

#### 1. Setup Backend
```bash
# From repository root
cd backend

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate # macOS/Linux

# Install backend dependencies
pip install -r requirements.txt

# Run backend test suite
cd ..
python scripts/test_safety_and_rag.py

# Start FastAPI server
python -m uvicorn backend.app.main:app --reload --port 8000
# Or simply:
python run_backend.py
```
The FastAPI backend will start at `http://localhost:8000`.  
Interactive Swagger API documentation: `http://localhost:8000/docs`.

#### 2. Setup Frontend
```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
The React frontend will be accessible at `http://localhost:5173`.

---

### Option 2: Docker Compose

```bash
docker-compose up --build
```
This spins up:
- PostgreSQL on port `5432`
- Qdrant Vector DB on port `6333`
- MindCare FastAPI Backend on port `8000`

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `LLM_PROVIDER` | LLM Provider (`gemini`, `openai`, `offline`) | `gemini` |
| `GEMINI_API_KEY` | Google Gemini API Key | *(Optional)* |
| `OPENAI_API_KEY` | OpenAI API Key | *(Optional)* |
| `DATABASE_URL` | PostgreSQL or SQLite connection string | `sqlite:///./mindcare.db` |
| `VECTOR_DATABASE_URL` | Remote Qdrant instance URL | *(Uses local disk storage if empty)* |
| `VECTOR_STORAGE_PATH` | Local Qdrant path | `./qdrant_storage` |
| `JWT_SECRET` | Secret key for JWT signing | `super-secret-mindcare-key...` |
| `EMBEDDING_MODEL` | HuggingFace embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| `TOP_K` | Number of chunks retrieved | `5` |
| `MAX_MEMORY_TURNS` | Number of conversational turns | `30` |

---

## 🧪 Verification & Testing

Run the automated test suite:
```bash
python scripts/test_safety_and_rag.py
```
This verifies:
1. **Crisis Safety System:** Suicide statements, self-harm, and immediate danger trigger the safety guardrail; non-crisis expressions (e.g. general sadness or exam stress) correctly avoid false positives.
2. **Auth & Security:** Password hashing with bcrypt, JWT token issuing and decoding.
3. **Database Memory & User Isolation:** Multi-turn persistence over 30 turns (60 messages), session renaming, deletion, and cross-user authorization enforcement.
4. **RAG Vector Search:** Ingestion of wellness resources and semantic search retrieval.

---

## 📋 API Endpoints

### Authentication
- `POST /api/auth/register` — Register a new account
- `POST /api/auth/login` — Login & receive JWT access token
- `POST /api/auth/logout` — Logout user
- `GET /api/auth/me` — Retrieve current authenticated user profile

### Chat & Sessions
- `POST /api/chat` — Send message (runs safety check, memory retrieval, RAG, and saves messages)
- `GET /api/chat/sessions` — List user's sessions
- `POST /api/chat/sessions` — Create a new conversation session
- `GET /api/chat/sessions/{session_id}` — Get session messages
- `PATCH /api/chat/sessions/{session_id}` — Rename session
- `DELETE /api/chat/sessions/{session_id}` — Delete session

### Knowledge Management
- `POST /api/knowledge/ingest` — Ingest curated knowledge library
- `POST /api/knowledge/upload` — Upload PDF/TXT/MD wellness documents
- `GET /api/knowledge/status` — Get vector collection stats
- `DELETE /api/knowledge/{document_id}` — Delete document chunks

### System
- `GET /api/health` — Service health check

