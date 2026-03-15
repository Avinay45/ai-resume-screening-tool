from utils.file_loader import load_resumes
from nlp.resume_parser import parse_resume
from rag.rag_pipeline import RAGPipeline
from utils.llm_evaluator import evaluate_candidate
import streamlit.web.cli as stcli
import sys

resume_files = load_resumes("data/resumes")

resumes = []

for file in resume_files:

    text = parse_resume(file)

    resumes.append((file, text))


rag = RAGPipeline()

rag.index_resumes(resumes)


job_description = """
Looking for a Data Analyst with Python,
SQL, Machine Learning and Data Visualization skills
"""


results = rag.retrieve_candidates(job_description)


print("\nTop Matching Candidates:\n")

for file_name, resume_text in results:

    print("Resume:", file_name)

    evaluation = evaluate_candidate(resume_text, job_description)

    print(evaluation)

    print("\n-----------------------\n")

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "ui/streamlit_ui.py"]
    sys.exit(stcli.main())