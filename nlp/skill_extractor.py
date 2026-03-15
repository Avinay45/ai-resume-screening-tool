import spacy

nlp = spacy.load("en_core_web_sm")

SKILL_SET = [
    "python",
    "java",
    "sql",
    "machine learning",
    "deep learning",
    "data analysis",
    "power bi",
    "tableau",
    "aws",
    "docker",
    "kubernetes",
    "tensorflow",
    "pytorch",
    "nlp",
    "pandas",
    "numpy",
    "scikit learn",
    "git",
    "linux"
]


def extract_skills(resume_text):

    doc = nlp(resume_text)

    extracted_skills = set()

    for token in doc:
        if token.text.lower() in SKILL_SET:
            extracted_skills.add(token.text.lower())

    for phrase in SKILL_SET:
        if phrase in resume_text:
            extracted_skills.add(phrase)

    return list(extracted_skills)