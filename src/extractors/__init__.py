from .pdf import extract_text_from_pdf
from .text import extract_text_from_text
from .word import extract_text_from_docx, extract_text_from_doc

__all__ = [
    "extract_text_from_pdf",
    "extract_text_from_text",
    "extract_text_from_docx",
    "extract_text_from_doc",
]
