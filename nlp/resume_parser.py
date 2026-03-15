import pdfplumber
import re

def extract_text_from_pdf(file_path):
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def clean_resume_text(text):

    # remove urls
    text = re.sub(r"http\S+", "", text)

    # remove special characters
    text = re.sub(r"[^A-Za-z0-9\s]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.lower()


def parse_resume(file_path):

    raw_text = extract_text_from_pdf(file_path)
    clean_text = clean_resume_text(raw_text)

    return clean_text