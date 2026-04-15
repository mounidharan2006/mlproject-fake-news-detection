import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

def create_pdf(username, real, fake):

    file_name = f"{username}_report.pdf"

    # 📊 GRAPH IMAGE
    plt.figure()
    plt.bar(["Real News", "Fake News"], [real, fake], color=["green", "red"])
    plt.title("Real vs Fake News Analysis")
    plt.ylabel("Count")

    graph_file = f"{username}_graph.png"
    plt.savefig(graph_file)
    plt.close()

    # 📄 PDF
    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()
    content = []

    # 🏢 HEADER + LOGO
    logo_path = "static/logo.png"

    if os.path.exists(logo_path):
        content.append(Image(logo_path, width=120, height=60))

    content.append(Paragraph("FAKE NEWS AI SYSTEM REPORT", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>User:</b> {username}", styles["Normal"]))
    content.append(Paragraph(f"<b>Date:</b> {datetime.now()}", styles["Normal"]))
    content.append(Spacer(1, 15))

    # 📊 GRAPH ADD
    content.append(Paragraph("Real vs Fake News Statistics", styles["Heading2"]))
    content.append(Spacer(1, 10))
    content.append(Image(graph_file, width=400, height=250))

    doc.build(content)

    return file_name