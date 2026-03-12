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

# ── Demo seed data — LOCKED, produces FitGuide AI concept ─────────────
DEMO_IDEAS = [
    {"text": "AI gym trainer",                        "type": "idea"},
    {"text": "people struggle with fitness consistency", "type": "problem"},
    {"text": "beginner workout confusion",            "type": "problem"},
    {"text": "habit tracking for workouts",           "type": "idea"},
    {"text": "AI voice coaching for fitness",         "type": "idea"},
]
DEMO_QUESTION = "fitness startup idea"


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

    # ── AI calls — each isolated so one failure never kills the response ──
    try:
        theme = infer_theme(related)
        if "error:" in theme:
            raise ValueError(theme)
    except Exception:
        theme = "AI unavailable — showing idea connections only"

    try:
        insight = generate_insight(related, question=data.question)
        if "error:" in insight:
            raise ValueError(insight)
    except Exception:
        insight = "AI unavailable — showing idea connections only"

    try:
        project = generate_project(related, question=data.question, theme=theme)
        if "error:" in project:
            raise ValueError(project)
    except Exception:
        project = "AI unavailable — showing idea connections only"

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
    """Seed memory with the locked demo dataset — idempotent. Returns the demo question too."""
    existing_texts = {m["text"].strip().lower() for m in get_all_memories()}
    added = 0
    for idea in DEMO_IDEAS:
        if idea["text"].strip().lower() not in existing_texts:
            add_memory(idea["text"], entry_type=idea["type"])
            added += 1
    return {
        "status":        "demo loaded",
        "ideas_added":   added,
        "memory_count":  memory_count(),
        "demo_question": DEMO_QUESTION,
    }


@app.get("/health")
def health():
    return {"status": "ok", "memory_count": memory_count()}
