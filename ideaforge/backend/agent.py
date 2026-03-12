import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Groq is OpenAI-compatible — just swap base_url and model
client  = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
MODEL   = "llama-3.3-70b-versatile"
TIMEOUT = 30  # seconds

# ── Static fallback — used when AI is unavailable ─────────────────────
# Written in the SAME format as the live prompt so the UI always parses it.
FALLBACK_PROJECT = """\
**Project Name**
AI Idea Connector

**Problem**
Users often capture raw ideas but fail to connect them into actionable projects. \
Without a system that finds relationships between thoughts, great ideas stay isolated \
and never become products.

**Solution**
IdeaForge stores every idea as a semantic vector, then uses AI to surface hidden \
connections and synthesise them into a structured startup concept automatically.

**Target Users**
Founders, hackers, and creative thinkers who want to turn scattered notes into real projects.

**Key Features**
- Semantic vector memory (ChromaDB)
- AI-powered idea connection graph
- One-click structured project generation
- 3-week MVP roadmap output

**Why This Idea Works**
Combining persistent memory with LLM reasoning creates a true second brain — one that \
remembers everything and reasons across all stored thoughts simultaneously. \
The result is always a concrete, actionable startup concept, not a generic suggestion.

**MVP Roadmap**
Week 1: Idea storage + semantic search
Week 2: Connection engine + theme detection
Week 3: Project generator + UI polish"""

FALLBACK_THEME   = "AI Productivity Tools"
FALLBACK_INSIGHT = """\
**Connection Insight**
The stored ideas all orbit a common problem: people have valuable thoughts but lack \
a system to connect and act on them. IdeaForge is that system.

**Hidden Opportunity**
Building an AI second-brain that auto-generates project concepts from raw notes \
could serve every knowledge worker who has ever had a great idea they never shipped."""


# ── Helpers ───────────────────────────────────────────────────────────

def _ideas_block(memories: list[dict]) -> str:
    if not memories:
        return "(no ideas stored yet)"
    return "\n".join(f"- [{m['type'].upper()}] {m['text']}" for m in memories)


def _chat(messages: list[dict], fallback: str) -> str:
    """Call Groq — return fallback on ANY error so the demo never crashes."""
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            timeout=TIMEOUT,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return fallback


# ── Public API ────────────────────────────────────────────────────────

def infer_theme(memories: list[dict]) -> str:
    """2–6 word theme label. Falls back to a clean static string."""
    if not memories:
        return FALLBACK_THEME

    prompt = f"""You are an AI Second Brain.

The user has stored these ideas:
{_ideas_block(memories)}

Identify the single core theme that connects them.
Respond with ONLY the theme — 2 to 6 words, no punctuation, no explanation."""

    return _chat([{"role": "user", "content": prompt}], fallback=FALLBACK_THEME)


def generate_insight(memories: list[dict], question: str = "") -> str:
    """Connection insight + hidden opportunity. Falls back to a parseable static string."""
    if not memories:
        return FALLBACK_INSIGHT

    prompt = f"""You are an AI Second Brain.

The user has stored the following ideas:
{_ideas_block(memories)}
{"The user asked: " + question if question else ""}

Respond with EXACTLY this structure — no other text:

**Connection Insight**
Explain in 2-3 sentences how these ideas relate to each other.

**Hidden Opportunity**
In 1-2 sentences, describe the opportunity revealed by combining them."""

    return _chat([{"role": "user", "content": prompt}], fallback=FALLBACK_INSIGHT)


def generate_project(memories: list[dict], question: str = "", theme: str | None = None) -> str:
    """Full structured startup concept. Falls back to a fully parseable static concept."""
    if not memories:
        return FALLBACK_PROJECT

    prompt = f"""You are IdeaForge, an AI startup generator.

Using these ideas:
{_ideas_block(memories)}
{"Core theme: " + theme if theme else ""}
{"User question: " + question if question else ""}

Return EXACTLY in this format — copy these headers word for word, no preamble, no sign-off:

**Project Name**
One catchy product name only — on the very next line after the header.

**Problem**
2-3 sentences on the real-world problem.

**Solution**
2-3 sentences on the AI-powered solution.

**Target Users**
1 sentence on who benefits.

**Key Features**
- Feature 1
- Feature 2
- Feature 3
- Feature 4

**Why This Idea Works**
2-3 sentences on why combining these ideas is powerful.

**MVP Roadmap**
Week 1: ...
Week 2: ...
Week 3: ..."""

    return _chat([{"role": "user", "content": prompt}], fallback=FALLBACK_PROJECT)
