import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ── System prompt: Second Brain Memory Agent ──────────────────────────
SYSTEM_PROMPT = """
You are an AI Second Brain Agent — a long-term memory and thinking partner.

Your purpose is NOT to simply answer questions. Your role is to:
1. Understand the user's new input (idea, note, question, link, or project concept).
2. Analyze the related past ideas provided to you.
3. Identify deep connections between the new input and past ideas.
4. Suggest evolved or combined ideas the user might not see themselves.
5. Encourage the user to think further.

ALWAYS respond using EXACTLY this structure (use the headers):

**New Entry Summary:**
Brief understanding of the new input.

**Relevant Past Ideas:**
List any past memories that relate (or say "None yet" if empty).

**Connection Insight:**
Explain HOW the ideas connect — similar topics, complementary tech, overlapping goals.

**Evolved Idea Suggestion:**
Propose a new or improved idea by combining the inputs.

**Next Thought Prompt:**
Ask the user one question that encourages deeper thinking.

IMPORTANT RULES:
- Prioritize discovering relationships across stored knowledge.
- If no connections exist, store the idea and encourage exploration.
- Focus on long-term thinking and idea evolution.
- Be specific and creative, not generic.
""".strip()


def analyze_new_idea(new_idea: str, past_memories: list[dict]) -> str:
    """When the user stores a new idea, check for connections with past memories."""
    if past_memories:
        past_block = "\n".join(
            f"- {m['text']} (similarity: {m['distance']})" for m in past_memories
        )
    else:
        past_block = "(no past ideas stored yet)"

    prompt = f"""
The user just saved a new idea:
"{new_idea}"

Here are their most related past ideas from memory:
{past_block}

Analyze this using the Second Brain framework.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def ask_second_brain(question: str, related_memories: list[dict]) -> str:
    """When the user asks a question, reason over stored memories."""
    if related_memories:
        mem_block = "\n".join(
            f"- {m['text']} (similarity: {m['distance']})" for m in related_memories
        )
    else:
        mem_block = "(no related ideas found in memory)"

    prompt = f"""
The user is asking their Second Brain:
"{question}"

Related ideas retrieved from memory:
{mem_block}

Analyze connections, generate insights, and suggest an evolved idea.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def infer_theme(memories: list[dict]) -> str:
    """Infer a short theme label from a set of ideas."""
    if not memories:
        return "No theme yet"

    ideas_text = "\n".join(f"- {m['text']}" for m in memories)
    prompt = f"""
Given these ideas:
{ideas_text}

Return a single short theme label (2-6 words). Example: "AI Fitness Coaching".
Only return the label, nothing else.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip().strip('"')


def generate_project(memories: list[dict], theme: str | None = None) -> str:
    """Generate a full project concept from connected ideas."""
    ideas_text = "\n".join(f"- {m['text']}" for m in memories)
    theme_line = f"\nDetected Theme: {theme}\n" if theme else ""

    prompt = f"""
You are an AI startup assistant and Second Brain Agent.

The user's connected ideas:
{ideas_text}
{theme_line}
Create a detailed project concept with:

1. **Project Name**
2. **Problem** — what real problem does this solve?
3. **Solution** — how does the product work?
4. **Target Users** — who benefits?
5. **Core Features** — list 4-5 key features
6. **Why This Matters** — one sentence on impact
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
