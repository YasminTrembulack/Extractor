from pathlib import Path
from typing import Callable, Dict, Optional

from src.extractors.pdf import extract_text_from_pdf
from src.extractors.text import extract_text_from_text
from src.extractors.word import extract_text_from_doc, extract_text_from_docx


SUPPORTED_FILE_TYPES: Dict[str, Callable[[bytes], str]] = {
    "application/pdf": extract_text_from_pdf,
    "text/plain": extract_text_from_text,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": extract_text_from_docx,  # .docx
    "application/msword": extract_text_from_doc,  # .doc
}

SUPPORTED_EXTENSIONS: Dict[str, Callable[[bytes], str]] = {
    ".pdf": extract_text_from_pdf,
    ".txt": extract_text_from_text,
    ".docx": extract_text_from_docx,
    ".doc": extract_text_from_doc,
}


class ExtractorFactory:

    def __init__(self):
        self._by_type = SUPPORTED_FILE_TYPES
        self._by_extension = SUPPORTED_EXTENSIONS

    def get_extractor(
        self, filename: str, content_type: str
    ) -> Optional[Callable[[bytes], str]]:

        if content_type in self._by_type:
            return self._by_type[content_type]

        extension = Path(filename).suffix.lower()
        if extension in self._by_extension:
            return self._by_extension[extension]

        return None
