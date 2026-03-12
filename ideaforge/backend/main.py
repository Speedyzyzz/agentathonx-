from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from memory import add_memory, search_memory, get_all_memories, memory_count, clear_all_memories
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

# ── Deterministic demo datasets — each produces a reliable AI output ──
DEMO_SETS = {
    "fitness": {
        "ideas": [
            {"text": "AI gym trainer",                            "type": "idea"},
            {"text": "people struggle with fitness consistency",  "type": "problem"},
            {"text": "beginner workout confusion",                "type": "problem"},
            {"text": "habit tracking for workouts",              "type": "idea"},
            {"text": "AI voice coaching for fitness",            "type": "idea"},
        ],
        "question": "fitness startup idea",
    },
    "education": {
        "ideas": [
            {"text": "students lose focus in online classes",     "type": "problem"},
            {"text": "AI tutoring for kids",                     "type": "idea"},
            {"text": "personalized learning pace",               "type": "idea"},
            {"text": "voice assistant for education",            "type": "idea"},
            {"text": "gamified learning app",                    "type": "idea"},
        ],
        "question": "education startup idea",
    },
    "startup": {
        "ideas": [
            {"text": "founders struggle validating ideas",        "type": "problem"},
            {"text": "AI that generates MVP plans",              "type": "idea"},
            {"text": "tools for startup market research",        "type": "idea"},
            {"text": "automated pitch deck builder",             "type": "idea"},
            {"text": "AI competitor analysis tool",             "type": "idea"},
        ],
        "question": "startup tools idea",
    },
    "productivity": {
        "ideas": [
            {"text": "people procrastinate on tasks",             "type": "problem"},
            {"text": "AI task prioritization assistant",         "type": "idea"},
            {"text": "calendar auto scheduling",                 "type": "idea"},
            {"text": "deep focus session tracker",               "type": "idea"},
            {"text": "AI productivity coach",                    "type": "idea"},
        ],
        "question": "productivity startup idea",
    },
}


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

    # _chat() in agent.py always returns a clean fallback on failure —
    # so these calls can never throw or return error strings.
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


@app.post("/demo/{demo_type}")
def load_demo_typed(demo_type: str):
    """Wipe memory and seed a named demo dataset. Returns the preset question."""
    if demo_type not in DEMO_SETS:
        raise HTTPException(status_code=404, detail=f"Unknown demo type '{demo_type}'. Available: {list(DEMO_SETS.keys())}")
    clear_all_memories()
    preset = DEMO_SETS[demo_type]
    for idea in preset["ideas"]:
        add_memory(idea["text"], entry_type=idea["type"])
    return {
        "status":   "loaded",
        "type":     demo_type,
        "count":    len(preset["ideas"]),
        "question": preset["question"],
    }


@app.post("/demo")
def load_demo():
    """Backward-compat alias — loads the fitness demo."""
    clear_all_memories()
    preset = DEMO_SETS["fitness"]
    for idea in preset["ideas"]:
        add_memory(idea["text"], entry_type=idea["type"])
    return {
        "status":        "demo loaded",
        "count":         len(preset["ideas"]),
        "demo_question": preset["question"],
    }


@app.post("/clear")
def clear_memory():
    """Wipe all memories — clean demo reset without restarting the server."""
    clear_all_memories()
    return {"status": "cleared", "memory_count": 0}


@app.get("/health")
def health():
    return {"status": "ok", "memory_count": memory_count()}
