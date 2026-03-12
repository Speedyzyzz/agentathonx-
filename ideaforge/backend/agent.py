# filepath: /Users/user/AgentathonX/ideaforge/backend/agent.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client  = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL   = "gpt-4o-mini"
TIMEOUT = 20  # seconds — prevents demo freezes


# ── Helpers ───────────────────────────────────────────────────────────

def _ideas_block(memories: list[dict]) -> str:
    if not memories:
        return "(no ideas stored yet)"
    return "\n".join(f"- [{m['type'].upper()}] {m['text']}" for m in memories)


def _chat(messages: list[dict], fallback: str) -> str:
    """Safe OpenAI call — returns fallback string on any error."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            timeout=TIMEOUT,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"{fallback} (error: {e})"


# ── Public functions ──────────────────────────────────────────────────

def infer_theme(memories: list[dict]) -> str:
    """Return a single short theme label that connects the ideas."""
    if not memories:
        return "No theme yet"

    prompt = f"""You are an AI Second Brain.

The user has stored these ideas:
{_ideas_block(memories)}

Identify the single core theme that connects them.
Respond with ONLY the theme — 2 to 6 words, no punctuation, no explanation."""

    return _chat(
        [{"role": "user", "content": prompt}],
        fallback="Mixed Ideas",
    )


def generate_insight(memories: list[dict], question: str = "") -> str:
    """Explain the connection between ideas and the opportunity they reveal."""
    if not memories:
        return "Add more ideas first, then ask IdeaForge to find connections."

    prompt = f"""You are an AI Second Brain.

The user has stored the following ideas:
{_ideas_block(memories)}

{"The user asked: " + question if question else ""}

Analyze the ideas and respond with exactly this structure:

**Connection Insight**
Explain in 2-3 sentences how these ideas relate to each other.

**Hidden Opportunity**
In 1-2 sentences, describe the opportunity revealed by combining them.

Be specific and creative, not generic."""

    return _chat(
        [{"role": "user", "content": prompt}],
        fallback="Could not generate insight.",
    )


def generate_project(memories: list[dict], question: str = "", theme: str | None = None) -> str:
    """Generate a full structured startup/project concept from connected ideas."""
    if not memories:
        return "No ideas stored yet. Add some ideas first!"

    prompt = f"""You are IdeaForge, an AI Second Brain that turns ideas into startup concepts.

The user has stored these ideas:
{_ideas_block(memories)}

{"Core theme: " + theme if theme else ""}
{"User question: " + question if question else ""}

Analyze the ideas and produce a full project concept using EXACTLY this format:

**Project Name**
A catchy, memorable name.

**Problem**
The real-world problem being solved (2-3 sentences).

**Solution**
The AI-powered solution (2-3 sentences).

**Target Users**
Who benefits from this (1 sentence).

**Key Features**
- Feature 1
- Feature 2
- Feature 3
- Feature 4

**Why This Idea Works**
Why combining these ideas is powerful (2-3 sentences).

**MVP Roadmap**
Week 1: ...
Week 2: ...
Week 3: ...

Be specific, practical, and exciting."""

    return _chat(
        [{"role": "user", "content": prompt}],
        fallback="Could not generate project concept.",
    )
