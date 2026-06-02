import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def generate_answer(question, context):

    prompt = f"""
You are a codebase assistant.

Question:
{question}

Retrieved Code:
{context}

Explain the answer clearly.
"""

    response = model.generate_content(prompt)

    return response.text