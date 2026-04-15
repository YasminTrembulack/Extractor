import logging
from typing import Any, Dict, List

from pinecone import Pinecone, ServerlessSpec

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.core.config import (
    PINECONE_API_KEY,
    PINECONE_CLOUD,
    PINECONE_INDEX_NAME,
    PINECONE_REGION,
)


class PineconeRepository:
    def __init__(self):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self._index = None

    @property
    def index(self):
        if self._index is None:
            self._index = self._get_or_create_index()
        return self._index

    def _get_or_create_index(self):
        if not self.pc.has_index(PINECONE_INDEX_NAME):
            try:
                logger.info(f"Creating index '{PINECONE_INDEX_NAME}'...")
                self.pc.create_index(
                    name=PINECONE_INDEX_NAME,
                    dimension=384,  # all-MiniLM-L6-v2 model dimension
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud=PINECONE_CLOUD or "aws",
                        region=PINECONE_REGION or "us-east-1",
                    ),
                )
                logger.info(f"Index '{PINECONE_INDEX_NAME}' created successfully!")
            except Exception as e:
                logger.error(f"Error creating index: {str(e)}")
                raise

        try:
            index = self.pc.Index(PINECONE_INDEX_NAME)
            logger.info(f"Connected to index '{PINECONE_INDEX_NAME}'")
            return index
        except Exception as e:
            logger.error(f"Error connecting to index: {str(e)}")
            raise

    def delete_vectors_by_metadata_field(self, value: str, field: str) -> int:
        """Delete vectors based on a specific metadata field value."""
        try:
            self.index.delete(filter={field: value})

        except Exception as e:
            logger.error(f"Error deleting vectors by metadata {field}: {str(e)}")
            raise

    def delete_vectors_by_id(self, id: str) -> int:
        """Delete vectors by their unique ID."""
        try:
            self.index.delete(id=id)
        except Exception as e:
            logger.error(f"Error deleting vectors by ID: {str(e)}")
            raise

    def replace_document_vectors(self, vectors: List[Dict[str, Any]]) -> None:
        """Replace document vectors in the index."""
        try:
            self.index.upsert(vectors=vectors)
        except Exception as e:
            logger.error(f"Error replacing document vectors: {str(e)}")
            raise

    def get_vector_by_id(self, id: str) -> Dict[str, Any]:
        try:
            result = self.index.fetch(ids=[id])
            return result.vectors.get(id)
        except Exception as e:
            logger.error(f"Error getting vectors by ID: {str(e)}")
            raise
