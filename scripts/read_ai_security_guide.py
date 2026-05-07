import pdfplumber
from pathlib import Path

pdf_path = "/Users/flyngcoq/AI_Project/40_Projects/Work/Safe_AI/인공지능(AI) 보안 안내서.pdf"

def extract_pdf_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

if __name__ == "__main__":
    if Path(pdf_path).exists():
        content = extract_pdf_text(pdf_path)
        # Output next 10000 characters for analysis
        print(content[10000:20000])
    else:
        print(f"File not found: {pdf_path}")
