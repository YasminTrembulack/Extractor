import io

import pdfplumber as pb


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extrai texto de um arquivo PDF."""
    with pb.open(io.BytesIO(file_bytes)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text
