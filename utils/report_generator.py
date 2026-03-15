from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def generate_report(candidate, score, evaluation):

    file_name = f"{candidate}_evaluation_report.pdf"

    c = canvas.Canvas(file_name, pagesize=letter)

    c.setFont("Helvetica", 12)

    y = 750

    c.drawString(50, y, f"Candidate Evaluation Report")
    y -= 40

    c.drawString(50, y, f"Candidate Name: {candidate}")
    y -= 30

    c.drawString(50, y, f"Candidate Score: {score}")
    y -= 40

    for line in evaluation.split("\n"):
        c.drawString(50, y, line)
        y -= 20

        if y < 100:
            c.showPage()
            y = 750

    c.save()

    return file_name