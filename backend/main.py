from fastapi import FastAPI
from dotenv import load_dotenv
from groq import Groq
import os

from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# =========================
# LOAD ENV
# =========================

load_dotenv()

# =========================
# FASTAPI APP
# =========================

app = FastAPI()

# =========================
# MEMORY STORE
# =========================

memory = {}

# =========================
# GROQ CLIENT
# =========================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# HOME ROUTE
# =========================

@app.get("/")
def home():

    return {
        "message": "EduAI Backend Running Successfully"
    }

# =========================
# NORMAL CHAT
# =========================

@app.get("/chat")
def chat(query: str):

    try:

        query_lower = query.lower()

        # =========================
        # SAVE MEMORY
        # =========================

        if "my name is" in query_lower:

            name = query_lower.replace(
                "my name is",
                ""
            ).strip()

            memory["name"] = name

            return {
                "response": f"Nice to meet you, {name} 😄"
            }

        # =========================
        # RECALL MEMORY
        # =========================

        if (
    "who am i" in query_lower
    or "who i am" in query_lower
    or "tell me who i am" in query_lower
    or "what is my name" in query_lower
):

            if "name" in memory:

                return {
                    "response": f"You are {memory['name']} 😄"
                }

            else:

                return {
                    "response": "I don't know your name yet 😅"
                }

        # =========================
        # NORMAL AI CHAT
        # =========================

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ]
        )

        answer = completion.choices[0].message.content

        return {
            "response": answer
        }

    except Exception as e:

        return {
            "response": str(e)
        }

# =========================
# PDF CHAT
# =========================

@app.get("/pdfchat")
def pdfchat(query: str, filename: str):
    try:
        pdf_path = f"frontend/uploads/{filename}"
        reader = PdfReader(pdf_path)
        pdf_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pdf_text += text

        prompt = f"""PDF Content:
{pdf_text[:3000]}

Question: {query}

Answer from PDF only."""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"response": completion.choices[0].message.content}

    except Exception as e:
        return {"response": str(e)}

    try:

        # PDF PATH
        pdf_path = f"frontend/uploads/{filename}"

        # READ PDF
        reader = PdfReader(pdf_path)

        pdf_text = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pdf_text += text

        # =========================
        # SPLIT TEXT INTO CHUNKS
        # =========================

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_text(pdf_text)

        # =========================
        # CREATE EMBEDDINGS
        # =========================

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # =========================
        # CREATE VECTOR STORE
        # =========================

        vectorstore = FAISS.from_texts(
            chunks,
            embedding=embeddings
        )

        # =========================
        # SEARCH RELEVANT CHUNK
        # =========================

        docs = vectorstore.similarity_search(query)

        context = docs[0].page_content

        # =========================
        # AI PROMPT
        # =========================

        prompt = f"""
        You are an AI tutor.

        Answer ONLY from the PDF content.

        Relevant PDF Content:
        {context}

        User Question:
        {query}
        """

        # =========================
        # AI RESPONSE
        # =========================

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = completion.choices[0].message.content

        return {
            "response": answer
        }

    except Exception as e:

        return {
            "response": str(e)
        }
    
# =========================
# SMART NOTES GENERATOR
# =========================

@app.get("/generate-notes")
def generate_notes(topic: str):

    try:

        prompt = f"""Create comprehensive and detailed study notes on the topic: {topic}

Use this exact format:

# {topic}

## Introduction
Write a detailed introduction of 5-6 lines covering what this topic is and why it is important.

## Background and History
Write 4-5 lines about the history or background of this topic.

## Key Concepts
- Concept 1: Write a detailed explanation of at least 2-3 sentences
- Concept 2: Write a detailed explanation of at least 2-3 sentences
- Concept 3: Write a detailed explanation of at least 2-3 sentences
- Concept 4: Write a detailed explanation of at least 2-3 sentences
- Concept 5: Write a detailed explanation of at least 2-3 sentences

## Detailed Explanation
Write at least 8-10 lines of thorough explanation covering all important aspects of the topic in simple English.

## Types and Classification
- Type 1: Explanation
- Type 2: Explanation
- Type 3: Explanation

## Real World Examples
- Example 1: Explain how this topic applies in real life
- Example 2: Explain how this topic applies in real life
- Example 3: Explain how this topic applies in real life

## Important Formulas or Rules (if applicable)
- Formula/Rule 1: Explanation
- Formula/Rule 2: Explanation

## Important Points to Remember
- Point 1
- Point 2
- Point 3
- Point 4
- Point 5

## Common Mistakes to Avoid
- Mistake 1: Explanation
- Mistake 2: Explanation
- Mistake 3: Explanation

## Summary
Write a thorough summary of 5-6 lines covering all main points.

## Practice Questions
1. Basic Question 1?
2. Basic Question 2?
3. Intermediate Question 3?
4. Intermediate Question 4?
5. Advanced Question 5?

STRICT RULES:
- Write in ENGLISH ONLY
- NO emojis
- NO Hindi words
- NO special symbols
- Use only plain English text
- Be thorough and detailed in every section
- Minimum 500 words total"""

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        notes = completion.choices[0].message.content

        return {
            "notes": notes
        }

    except Exception as e:

        return {
            "notes": f"Error: {str(e)}"
        }
    
    # =========================
# FLASHCARD GENERATOR
# =========================

@app.get("/generate-flashcards")
def generate_flashcards(topic: str):

    try:

        prompt = f"""Create 15 detailed flashcards on the topic: {topic}

Return ONLY a JSON array in this exact format, nothing else:
[
    {{"question": "What is ...?", "answer": "Detailed answer here with proper explanation in 2-3 sentences"}},
    {{"question": "What is ...?", "answer": "Detailed answer here with proper explanation in 2-3 sentences"}}
]

STRICT RULES:
- Return ONLY the JSON array
- NO extra text before or after
- NO emojis
- NO Hindi words
- English only
- Exactly 15 flashcards
- Questions should be meaningful and thought provoking
- Answers should be detailed, minimum 2-3 sentences
- Cover basic, intermediate and advanced concepts of the topic"""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        import re

        raw = completion.choices[0].message.content
        match = re.search(r'\[.*\]', raw, re.DOTALL)

        if match:
            cards = json.loads(match.group())
        else:
            cards = []

        return {"flashcards": cards}

    except Exception as e:
        return {"flashcards": [], "error": str(e)}


# =========================
# MINDMAP GENERATOR
# =========================

@app.get("/generate-mindmap")
def generate_mindmap(topic: str):

    try:

        prompt = f"""Create a detailed mindmap structure on the topic: {topic}

Return ONLY a JSON object in this exact format, nothing else:
{{
    "center": "{topic}",
    "branches": [
        {{
            "title": "Branch Title",
            "points": ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5"]
        }}
    ]
}}

STRICT RULES:
- Return ONLY the JSON object
- NO extra text before or after
- NO emojis
- NO Hindi words
- English only
- Exactly 6 branches
- Exactly 5 detailed points per branch
- Points should be descriptive, not just 2-3 words
- Cover the topic thoroughly and in depth"""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        import re

        raw = completion.choices[0].message.content
        match = re.search(r'\{.*\}', raw, re.DOTALL)

        if match:
            mindmap = json.loads(match.group())
        else:
            mindmap = {}

        return {"mindmap": mindmap}

    except Exception as e:
        return {"mindmap": {}, "error": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)