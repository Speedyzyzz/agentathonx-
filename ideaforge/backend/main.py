from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from memory import add_memory, search_memory, get_all_memories, memory_count
from agent import (
    analyze_new_idea,
    ask_second_brain,
    infer_theme,
    generate_project,
)

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


# ── Models ────────────────────────────────────────────────────────────
class Idea(BaseModel):
    text: str
    type: str = "idea"          # idea | note | link | project


class Query(BaseModel):
    question: str


# ── Endpoints ─────────────────────────────────────────────────────────
@app.post("/add")
def add_idea(data: Idea):
    """Store a new idea and get immediate Second Brain analysis."""
    # Search for related memories BEFORE storing (so we don't match itself)
    related = search_memory(data.text, n_results=5)

    # Store the new idea
    doc_id = add_memory(data.text, entry_type=data.type)

    # Analyze connections
    analysis = analyze_new_idea(data.text, related)

    return {
        "status": "idea stored",
        "id": doc_id,
        "memory_count": memory_count(),
        "related_memories": related,
        "analysis": analysis,
    }


@app.post("/ask")
def ask_question(data: Query):
    """Ask the Second Brain — retrieve memories, detect theme, generate project."""
    related = search_memory(data.question, n_results=5)

    # Second Brain reasoning
    insight = ask_second_brain(data.question, related)

    # Theme detection
    theme = infer_theme(related)

    # Full project generation
    project = generate_project(related, theme=theme)

    return {
        "related_ideas": [m["text"] for m in related],
        "theme": theme,
        "insight": insight,
        "project": project,
    }


@app.get("/memories")
def list_memories():
    """Return all stored memories (for the UI memory bank)."""
    return {
        "count": memory_count(),
        "memories": get_all_memories(),
    }


@app.get("/health")
def health():
    return {"status": "ok", "memories": memory_count()}
