import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def evaluate_candidate(resume_text, job_description):

    prompt = f"""
You are an AI recruiter.

Evaluate the candidate resume against the job description.

Job Description:
{job_description}

Resume:
{resume_text}

Return the result in this format:

Candidate Score: <0-100>

Matching Skills:
- skill1
- skill2

Missing Skills:
- skill1
- skill2

Recommendation:
<short hiring recommendation>
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content