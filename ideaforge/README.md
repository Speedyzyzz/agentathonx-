# 🧠 IdeaForge — AI Second Brain Agent

> "ChatGPT answers questions. IdeaForge connects your thoughts and turns them into real projects."

An AI-powered **Second Brain** that stores your ideas, discovers hidden semantic connections, and generates full startup concepts — using ChromaDB vector memory and GPT-4o-mini reasoning.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Browser  (HTML + Tailwind + GSAP) │
│  Add Idea │ Memory Bank │ Ask AI    │
│  Connection Graph │ AI Response     │
└──────────────┬──────────────────────┘
               │  HTTP (fetch)
               ▼
┌─────────────────────────────────────┐
│          FastAPI  Backend           │
│                                     │
│  main.py   — REST API + CORS        │
│  memory.py — ChromaDB vector store  │
│  agent.py  — GPT-4o-mini reasoning  │
└───────────────┬─────────────────────┘
                │
        ┌───────┴───────┐
        ▼               ▼
   ChromaDB          OpenAI
 (vector store)   (gpt-4o-mini)
```

---

## ✨ How It Works

| Step | Action |
|------|--------|
| 1. **Store** | User saves ideas, notes, problems, or solutions via `/add` — instant, no AI call |
| 2. **Search** | `/ask` runs semantic vector search (n=8) to retrieve the most related memories |
| 3. **Theme** | LLM infers the single core theme connecting the ideas |
| 4. **Insight** | LLM explains how the ideas connect and what opportunity they reveal |
| 5. **Generate** | LLM produces a full structured startup concept with features + MVP roadmap |
| 6. **Visualise** | Canvas graph renders nodes + connections |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, Tailwind CSS, GSAP 3, Canvas API |
| Backend | Python 3.13, FastAPI, Uvicorn |
| Memory | ChromaDB (in-memory vector embeddings) |
| AI | OpenAI GPT-4o-mini |

---

## 🚀 Setup & Run

### 1. Clone

```bash
git clone https://github.com/Speedyzyzz/agentathonx-.git
cd agentathonx-/ideaforge
```

### 2. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:

```
OPENAI_API_KEY=sk-your-key-here
```

Start the server:

```bash
uvicorn main:app --reload
```

Backend: **http://127.0.0.1:8000**  
API docs: **http://127.0.0.1:8000/docs**

### 3. Frontend

```bash
cd ../frontend
python3 -m http.server 3000
```

Open **http://localhost:3000**

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/add` | Store an idea instantly (no AI, sub-100ms) |
| `POST` | `/ask` | Search memory + run full AI reasoning pipeline |
| `POST` | `/demo` | Seed 5 fitness demo ideas (idempotent) |
| `GET`  | `/memories` | List all stored memories (newest first) |
| `GET`  | `/stats` | Live memory count for UI badge |
| `GET`  | `/health` | Health check |

### POST `/add`

```bash
curl -X POST http://127.0.0.1:8000/add \
  -H "Content-Type: application/json" \
  -d '{"text": "AI gym trainer", "type": "idea"}'
# → { "status": "stored", "id": "...", "memory_count": 1 }
```

### POST `/ask`

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "fitness startup idea"}'
# → { "theme": "...", "related_ideas": [...], "insight": "...", "project": "..." }
```

---

## 🎬 Demo Flow (2 minutes)

### One-click seed (recommended for demo)

1. Click **🏋️ Load fitness ideas** in the workspace
2. Type `fitness startup idea` in Ask AI
3. Click **Generate Project**

### Manual flow

Add these ideas:

```
💡 AI gym trainer
❗ people struggle with gym consistency
❗ beginner workout confusion
💡 fitness habit tracking
💡 AI habit reminders
```

Ask: **`fitness startup idea`**

Expected output:
- **Theme** — AI-Powered Fitness Coaching
- **Retrieved Ideas** — all ideas shown as tags
- **Connection Insight** — how they relate + opportunity
- **Project Concept** — name, problem, solution, features, MVP roadmap
- **Graph** — nodes connected in canvas visualisation

---

## 🧠 Agent Design

Three focused functions in `agent.py`:

| Function | Purpose |
|----------|---------|
| `infer_theme()` | Returns a 2–6 word theme label |
| `generate_insight()` | Explains connections + hidden opportunity |
| `generate_project()` | Full structured startup concept |

All calls use `timeout=20` and `try/except` — the demo **never crashes**.

---

## 🔒 Safeguards

- `/add` rejects ideas > 500 characters with a clear error
- All OpenAI calls return a graceful fallback on any error
- `/demo` is idempotent — repeated calls won't create duplicates
- Search deduplicates results before passing to LLM

---

## 📁 Project Structure

```
ideaforge/
├── README.md
├── backend/
│   ├── main.py          # FastAPI routes
│   ├── memory.py        # ChromaDB vector store
│   ├── agent.py         # OpenAI reasoning pipeline
│   ├── requirements.txt
│   └── .env             # OPENAI_API_KEY (not committed)
└── frontend/
    └── index.html       # Full SPA — landing page + live workspace
```

---

## 💬 Pitch Line

> *"IdeaForge is not a chatbot. It's a digital thinking partner — it remembers everything you've ever thought, finds the connections you missed, and turns your scattered ideas into real startup concepts."*

---

## 📄 License

MIT — built for Agentathon X by **Speedyzyzz**
