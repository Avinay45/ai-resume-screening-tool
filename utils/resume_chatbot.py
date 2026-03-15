import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_resume_chatbot(question, resume_context):

    prompt = f"""
You are an AI hiring assistant.

Use the following candidate resume information to answer the recruiter question.

Resume Context:
{resume_context}

Recruiter Question:
{question}

Provide a clear and helpful answer.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content