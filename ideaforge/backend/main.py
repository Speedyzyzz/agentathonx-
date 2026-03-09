from fastapi import FastAPI
from pydantic import BaseModel
from memory import add_memory, search_memory
from agent import generate_project, infer_theme

app = FastAPI()


class Idea(BaseModel):
    text: str


class Query(BaseModel):
    question: str


@app.post("/add")
def add_idea(data: Idea):
    add_memory(data.text)
    return {"status": "idea stored"}


@app.post("/ask")
def ask_question(data: Query):
    ideas = search_memory(data.question)

    theme = infer_theme(ideas)
    project = generate_project(ideas, theme=theme)

    return {"related_ideas": ideas, "theme": theme, "project": project}
