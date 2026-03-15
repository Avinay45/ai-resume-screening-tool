import os

def load_resumes(folder_path):

    resume_files = []

    for file in os.listdir(folder_path):

        if file.endswith(".pdf"):
            resume_files.append(os.path.join(folder_path, file))

    return resume_files