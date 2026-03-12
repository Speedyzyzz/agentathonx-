# 🧠 IdeaForge — AI Second Brain Agent

> "ChatGPT answers questions. IdeaForge connects your thoughts and turns them into real projects."

An AI-powered **Second Brain** that stores your ideas, discovers hidden connections across time, and generates evolved project concepts — all using semantic vector memory and LLM reasoning.

## Architecture

```
┌─────────────────────────────────┐
│       Browser (HTML + Tailwind) │
│  Memory Bank │ Graph │ Agent UI │
└────────────┬────────────────────┘
             │  POST /add, /ask, /memories
             ▼
┌─────────────────────────────────┐
│        FastAPI Backend          │
│                                 │
│  main.py    — API + CORS        │
│  memory.py  — ChromaDB vectors  │
│  agent.py   — Second Brain LLM  │
└─────────────────────────────────┘
         │              │
         ▼              ▼
   ChromaDB          OpenAI
  (vector store)   (gpt-4o-mini)
```

## How It Works

1. **Store** — User saves ideas, notes, links, or project concepts.
2. **Analyze** — Agent immediately searches memory for related past ideas.
3. **Connect** — Agent identifies relationships (similar topics, complementary tech, overlapping goals).
4. **Evolve** — Agent suggests combined/improved ideas the user might not see.
5. **Generate** — On `/ask`, agent clusters ideas by theme and generates a full startup concept.

## Agent Response Format

Every response follows the **Second Brain** framework:

- **New Entry Summary** — what the user just said
- **Relevant Past Ideas** — related memories retrieved via vector search
- **Connection Insight** — how the ideas link together
- **Evolved Idea Suggestion** — a new combined idea
- **Next Thought Prompt** — a question to push thinking further

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, Tailwind CSS, Canvas (connection graph) |
| Backend | Python, FastAPI |
| Memory | ChromaDB (vector embeddings) |
| AI | OpenAI GPT-4o-mini |

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env`:

```
OPENAI_API_KEY=your_key_here
```

Run:

```bash
uvicorn main:app --reload
```

Open `frontend/index.html` in your browser.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/add` | Store idea + get Second Brain analysis |
| POST | `/ask` | Ask a question → retrieve, reason, generate |
| GET | `/memories` | List all stored memories |
| GET | `/health` | Health check + memory count |

## Demo Script (2 minutes)

**1) Add ideas:**
- "AI gym trainer"
- "people struggle with gym consistency"
- "beginner workout confusion"
- "fitness habit tracking"

Watch the agent find connections after each save.

**2) Ask:** "fitness startup idea"

**3) Show:**
- Retrieved ideas (vector search)
- Detected theme
- Second Brain insight (connections)
- Generated project concept
- Connection graph visualization

**Pitch line:**

> "IdeaForge turns scattered thoughts into real startup concepts using semantic memory. It's not a chatbot — it's a digital thinking partner."

## License

MIT
