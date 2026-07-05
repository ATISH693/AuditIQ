import pdfplumber

def extract_pdf_text(file) -> str:

    extracted_text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

    return extracted_text