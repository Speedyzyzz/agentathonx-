# IdeaForge

AI that stores ideas, finds connections, and generates project concepts.

## Architecture

```
Browser (HTML)
  │  POST /add, /ask
  ▼
FastAPI backend
  ├─ memory.py  (ChromaDB vector store)
  └─ agent.py   (LLM: theme + project concept)
```

## Setup (macOS / zsh)

### 1) Backend

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

In VS Code: **Python: Select Interpreter** → choose `backend/venv`.

Run the API:

```bash
uvicorn main:app --reload
```

Open docs:
- http://127.0.0.1:8000/docs

### 2) Frontend

Open `frontend/index.html` in your browser.

## Demo script

1. Add 3–5 ideas
   - "AI gym trainer"
   - "people struggle with gym consistency"
   - "beginner workout confusion"
2. Ask: "fitness startup idea"
3. Show:
   - retrieved ideas
   - inferred theme
   - generated project concept

Pitch line:

> IdeaForge turns scattered thoughts into real startup concepts using semantic memory.
