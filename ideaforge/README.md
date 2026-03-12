# 🧠 IdeaForge — AI Second Brain Agent

> "ChatGPT answers questions. IdeaForge connects your thoughts and turns them into real projects."

An AI-powered **Second Brain** that stores your ideas, discovers hidden semantic connections, and generates full startup concepts — using **ChromaDB vector memory** and **Llama-3.3-70b** (via Groq) for reasoning.

---

## 🤖 AI Pipeline

Ideas flow through four deterministic stages — no black box, no hallucination loop:

```
Raw Ideas
   ↓
Vector Memory  (ChromaDB — stores each idea as a semantic embedding)
   ↓
Semantic Retrieval  (cosine similarity search, top-8 results)
   ↓
LLM Reasoning  (Llama-3.3-70b via Groq — theme + insight + project)
   ↓
Structured Startup Concept + MVP Roadmap
```

Each stage is **independently observable** in the UI:
- Memory Bank shows all stored vectors
- AI Reasoning panel shows which vectors were retrieved + relevance score bars
- Connection Insight explains the pattern the AI found
- Generated Project renders every structured section individually

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────┐
│   Browser  (HTML + Tailwind CSS + GSAP) │
│                                         │
│  Add Idea │ Memory Bank │ Ask AI        │
│  AI Reasoning │ Connection Graph        │
│  Generated Project + MVP Roadmap        │
└──────────────────┬──────────────────────┘
                   │  HTTP (fetch)
                   ▼
┌─────────────────────────────────────────┐
│           FastAPI  Backend              │
│                                         │
│  main.py   — REST API + CORS            │
│  memory.py — ChromaDB vector store      │
│  agent.py  — Llama-3.3-70b reasoning    │
└──────────────┬──────────────────────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
  ChromaDB           Groq API
(vector store)   (llama-3.3-70b-versatile)
```

---

## ✨ How It Works

| Step | Action |
|------|--------|
| 1. **Store** | User saves ideas via `/add` — instant vector embedding, no AI call, sub-100ms |
| 2. **Retrieve** | `/ask` runs cosine similarity search (n=8) to find the most semantically related memories |
| 3. **Theme** | LLM infers the single core theme connecting the retrieved ideas |
| 4. **Insight** | LLM explains how the ideas connect and what opportunity they reveal |
| 5. **Generate** | LLM produces a fully structured startup concept: name, problem, solution, features, MVP roadmap |
| 6. **Visualise** | Canvas graph renders idea nodes + weighted connections |

---

## 🎬 Example Flow

A user adds several rough ideas:

- AI gym trainer
- workout habit tracking
- beginner workout confusion
- voice coaching for fitness
- people struggle with consistency

IdeaForge stores each idea as a **vector embedding** in ChromaDB. When the user asks a question, it retrieves the most semantically relevant ones via cosine similarity.

**User asks:** `"fitness startup idea"`

**Retrieved memories (AI Reasoning panel)**

| Memory | Type | Relevance |
|--------|------|-----------|
| AI gym trainer | idea | ████████████ 100% |
| voice coaching for fitness | idea | █████████░░░ 78% |
| people struggle with consistency | problem | ███████░░░░░ 64% |
| beginner workout confusion | problem | ██████░░░░░░ 55% |
| workout habit tracking | idea | █████░░░░░░░ 48% |

These retrieved memories become the **entire reasoning context** passed to the LLM — no extra prompting, no static injection.

---

### AI Response

IdeaForge generates a fully structured startup concept:

**🎯 Theme**
> Personal AI Fitness Coaching

**🔗 Connection Insight**
> Many people struggle to stay consistent with workouts because they lack personalised guidance, accountability, and real-time feedback. These ideas collectively point to an AI system that acts as a personal trainer — adapting to user behaviour, tracking habits, and coaching in real time.

**Project Name**
> FitForge AI

**❗ Problem**
> Most fitness apps provide static workout plans and require users to stay self-motivated. Beginners especially struggle with confusion about where to start, leading to high dropout rates within the first few weeks.

**✅ Solution**
> An AI-driven fitness assistant that provides real-time voice coaching, tracks workout habits, and continuously adapts recommendations based on user behaviour and progress.

**⚡ Key Features**
- AI voice coaching during workouts
- Personalised workout generation
- Habit tracking and progress feedback
- Beginner-friendly onboarding flow
- Smart reminders and motivation nudges

**🗓️ MVP Roadmap**

| Week | Milestone |
|------|-----------|
| Week 1 | Build workout generator and basic habit tracking |
| Week 2 | Add AI voice coaching and progress analytics |
| Week 3 | Release prototype with personalised adaptive plans |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, Tailwind CSS v3, GSAP 3.12, Canvas API |
| Backend | Python 3.13, FastAPI, Uvicorn |
| Memory | ChromaDB (in-memory vector embeddings) |
| LLM | Llama-3.3-70b-versatile via Groq API |
| HTTP Client | OpenAI SDK (pointed at `api.groq.com/openai/v1`) |

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
GROQ_API_KEY=your-groq-key-here
```

Start the server:

```bash
uvicorn main:app --reload
```

Backend: **http://127.0.0.1:8000**  
API docs: **http://127.0.0.1:8000/docs**

### 3. Frontend

Open `frontend/index.html` directly in a browser — or serve it:

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
| `POST` | `/ask` | Semantic search + full AI reasoning pipeline |
| `POST` | `/demo/{type}` | Seed a named demo dataset (fitness / education / startup / productivity) |
| `POST` | `/clear` | Wipe all memories |
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
```

Response:
```json
{
  "theme": "Personal AI Fitness Coaching",
  "related_ideas": ["AI gym trainer", "..."],
  "memories_used": [
    { "text": "AI gym trainer", "type": "idea", "distance": 0.31 }
  ],
  "insight": "These ideas share a core theme of...",
  "project": "**Project Name**\nFitForge AI\n\n**Problem**\n..."
}
```

### POST `/demo/{type}`

```bash
curl -X POST http://127.0.0.1:8000/demo/fitness
# → { "status": "loaded", "type": "fitness", "count": 5, "question": "fitness startup idea" }
```

Available types: `fitness` · `education` · `startup` · `productivity`

---

## 🎮 Demo Flow

### One-click (recommended for judges)

1. Open `frontend/index.html`
2. Memory bank is **pre-loaded** with 5 fitness ideas on arrival
3. Click any demo button: **🏋️ Fitness AI**, **🎓 Education AI**, **🚀 Startup Builder**, or **⚡ Productivity AI**
4. Watch the 5-stage reasoning pipeline run live
5. Read the structured startup concept that appears

### Manual flow

Add ideas in the workspace:

```
💡 AI gym trainer
❗ people struggle with gym consistency
❗ beginner workout confusion
💡 fitness habit tracking
💡 AI voice coaching
```

Ask: **`fitness startup idea`**

---

## 🧠 Agent Design

Three focused functions in `agent.py`, each with `timeout=30` and a static fallback that always parses correctly:

| Function | Input | Output |
|----------|-------|--------|
| `infer_theme()` | Retrieved memories | 2–6 word theme label |
| `generate_insight()` | Retrieved memories + question | Paragraph explaining connections + opportunity |
| `generate_project()` | Retrieved memories + question + theme | Full structured startup concept with `**Section**` headers |

All Groq calls use the OpenAI SDK with `base_url="https://api.groq.com/openai/v1"` — no custom HTTP client needed.

---

## 🔒 Safeguards

- `/add` rejects ideas > 500 characters with HTTP 400
- All LLM calls return a static structured fallback on any error — the demo **never crashes**
- `/demo/{type}` always wipes memory before reseeding — idempotent, no duplicates
- ChromaDB search deduplicates results before passing to the LLM
- Frontend reads memory count from `GET /stats` API directly — never from stale DOM text

---

## 📁 Project Structure

```
ideaforge/
├── README.md
├── backend/
│   ├── main.py          # FastAPI routes + demo datasets
│   ├── memory.py        # ChromaDB vector store
│   ├── agent.py         # Groq / Llama-3.3-70b reasoning pipeline
│   ├── requirements.txt
│   └── .env             # GROQ_API_KEY (not committed)
└── frontend/
    └── index.html       # Full SPA — landing page + live workspace
```

---

*Built for AgentathonX by [Speedyzyzz](https://github.com/Speedyzyzz)*
