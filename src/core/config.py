import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuração centralizada da aplicação."""

    # Pinecone
    PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "default-index")
    PINECONE_CLOUD: str = os.getenv("PINECONE_CLOUD", "aws")
    PINECONE_REGION: str = os.getenv("PINECONE_REGION", "us-east-1")

    # Validações
    def __init__(self):
        if not self.PINECONE_API_KEY:
            raise RuntimeError("PINECONE_API_KEY must be set in the environment")


# Instância global
config = Config()

# Para compatibilidade
PINECONE_API_KEY = config.PINECONE_API_KEY
PINECONE_INDEX_NAME = config.PINECONE_INDEX_NAME
PINECONE_CLOUD = config.PINECONE_CLOUD
PINECONE_REGION = config.PINECONE_REGION
