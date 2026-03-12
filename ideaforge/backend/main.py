from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from memory import add_memory, search_memory, get_all_memories, memory_count
from agent import infer_theme, generate_project, generate_insight

app = FastAPI(
    title="IdeaForge — Second Brain Agent",
    description="AI that stores ideas, finds connections, and generates project concepts.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Demo seed data ─────────────────────────────────────────────────────
DEMO_IDEAS = [
    {"text": "AI gym trainer",                           "type": "idea"},
    {"text": "people struggle with fitness consistency", "type": "problem"},
    {"text": "beginner workout confusion",               "type": "problem"},
    {"text": "fitness habit tracking app",               "type": "idea"},
    {"text": "AI habit reminders via SMS",               "type": "idea"},
]


# ── Models ────────────────────────────────────────────────────────────
class Idea(BaseModel):
    text: str
    type: str = "idea"  # idea | note | link | problem | solution | project


class Query(BaseModel):
    question: str


# ── Endpoints ─────────────────────────────────────────────────────────

@app.post("/add")
def add_idea(data: Idea):
    """Store a new idea instantly — NO LLM call here, always sub-100ms."""
    if len(data.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Idea text cannot be empty.")
    if len(data.text) > 500:
        raise HTTPException(status_code=400, detail="Idea too long (max 500 chars).")

    doc_id = add_memory(data.text.strip(), entry_type=data.type)

    return {
        "status": "stored",
        "id": doc_id,
        "memory_count": memory_count(),
    }


@app.post("/ask")
def ask_question(data: Query):
    """Ask the Second Brain — all AI reasoning happens only here."""
    if len(data.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    related = search_memory(data.question, n_results=8)

    theme   = infer_theme(related)
    insight = generate_insight(related, question=data.question)
    project = generate_project(related, question=data.question, theme=theme)

    return {
        "theme":         theme,
        "related_ideas": [m["text"] for m in related],
        "insight":       insight,
        "project":       project,
    }


@app.get("/memories")
def list_memories():
    return {"count": memory_count(), "memories": get_all_memories()}


@app.get("/stats")
def stats():
    """Memory stats — useful for the UI badge."""
    return {"memory_count": memory_count()}


@app.post("/demo")
def load_demo():
    """Seed the memory with demo fitness ideas — one-click hackathon demo."""
    for idea in DEMO_IDEAS:
        add_memory(idea["text"], entry_type=idea["type"])
    return {"status": "demo loaded", "ideas_added": len(DEMO_IDEAS), "memory_count": memory_count()}


@app.get("/health")
def health():
    return {"status": "ok", "memory_count": memory_count()}
