import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def infer_theme(ideas):
    prompt = f"""
You are an assistant that labels themes.

Given these ideas:
{ideas}

Return a single short theme label (2-6 words). Example: "AI Fitness Coaching".
Only return the label.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip().strip('"')


def generate_project(ideas, theme=None):
    theme_line = f"\nTheme: {theme}\n" if theme else ""

    prompt = f"""
You are an AI startup assistant.

Given these related ideas:

{ideas}
{theme_line}
Create a project concept with:

1. Project Name
2. Problem
3. Solution
4. Target Users
5. Core Features
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content
