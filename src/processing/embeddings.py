from typing import List, Optional

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()


class EmbeddingService:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._embeddings_model: Optional[HuggingFaceEmbeddings] = None

    @property
    def embeddings_model(self) -> HuggingFaceEmbeddings:
        """Lazy loading do modelo de embeddings."""
        if self._embeddings_model is None:
            self._embeddings_model = HuggingFaceEmbeddings(model_name=self.model_name)
        return self._embeddings_model

    def generate_embeddings(self, chunks: List[str]) -> List[List[float]]:
        """Gera embeddings para uma lista de chunks de texto."""
        if isinstance(chunks, str):
            texts = [chunks]
        else:
            texts = chunks

        vectors = self.embeddings_model.embed_documents(texts)
        return [list(map(float, vector)) for vector in vectors]
