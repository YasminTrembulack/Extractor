def extract_text_from_text(file_bytes: bytes) -> str:
    """Extrai texto de um arquivo de texto simples."""
    return file_bytes.decode("utf-8", errors="replace")
