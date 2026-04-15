import io

from docx import Document


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extrai texto de um arquivo .docx."""
    doc = Document(io.BytesIO(file_bytes))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def extract_text_from_doc(file_bytes: bytes) -> str:
    """Extrai texto de um arquivo .doc (formato antigo)."""
    # .doc é um formato antigo e complexo de extrair
    # Recomendação: converter manualmente para .docx antes de fazer upload
    return "Arquivo .doc detectado. Para processar arquivos .doc, converta para .docx primeiro usando Microsoft Word ou ferramentas online gratuitas."
