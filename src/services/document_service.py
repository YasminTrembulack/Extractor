import logging

from datetime import datetime

from src.core.models import UploadPayload
from src.extractors.extractor_factory import ExtractorFactory
from src.extractors.extractor_factory import ExtractorFactory
from src.processing import TextChunker, EmbeddingService
from src.repository.pinecode_repository import PineconeRepository

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self):
        self.chunker = TextChunker()
        self.extractor_factory = ExtractorFactory()
        self.embedding_service = EmbeddingService()
        self.repository: PineconeRepository = PineconeRepository()

    def process_file_upload(self, payload: UploadPayload) -> int:
        extractor = self.extractor_factory.get_extractor(
            payload.filename, payload.content_type
        )
        if extractor is None:
            return 0  # Type not supported, skip processing

        text = extractor(payload.file_bytes)
        chunks = self.chunker.chunk_text(text)

        # Cleans up extra chunks that may not be updated if the number of chunks is smaller than before
        self._cleanup_extra_chunks(new_total_chunks=len(chunks), id=payload.id)

        embeddings = self.embedding_service.generate_embeddings(chunks)

        vectors = self._build_vectors(chunks, embeddings, payload)
        self.repository.replace_document_vectors(vectors)

        return len(vectors)

    def delete_vectors_by_ids(self, ids: list[str]) -> None:
        logger.info(f"Initializing deletion of {len(ids)} document(s).")

        for doc_id in ids:
            self.repository.delete_vectors_by_metadata_field(doc_id, "id")

        logger.info(f"Deletion completed: {len(ids)} vectors deleted")

    def _cleanup_extra_chunks(self, new_total_chunks: int, id: str) -> None:
        """Remove chunks that are no longer needed when a document is updated with fewer chunks."""
        first_chunk = self.repository.get_vector_by_id(f"{id}_0")
        if not first_chunk:
            return  # No existing chunks, nothing to clean up

        old_total_chunks = (
            first_chunk.metadata.get("total_chunks", 0) if first_chunk.metadata else 0
        )

        if old_total_chunks <= new_total_chunks:
            return  # No extra chunks to delete

        delete_count = old_total_chunks - new_total_chunks
        logger.info(f"Cleaning up {delete_count} extra chunk(s) for document ID '{id}'")

        for chunk_index in range(new_total_chunks, old_total_chunks):
            chunk_id = f"{id}_{chunk_index}"
            self.repository.delete_vectors_by_id(chunk_id)

    def _build_vectors(
        self, chunks: list[str], embeddings: list[list[float]], payload: UploadPayload
    ) -> list[dict]:
        if len(chunks) != len(embeddings):
            raise ValueError("Number of embeddings does not match number of chunks")

        created_at = datetime.now()
        updated_at = created_at

        base = payload.id or payload.filename

        return [
            {
                "id": f"{payload.id}_{index}",
                "values": embedding,
                "metadata": {
                    "text": chunk,
                    "id": payload.id,
                    "chunk_index": index,
                    "total_chunks": len(chunks),
                    "filename": payload.filename,
                    "filepath": payload.filepath,
                    "created_at": created_at.isoformat(),
                    "updated_at": updated_at.isoformat(),
                },
            }
            for index, (chunk, embedding) in enumerate(zip(chunks, embeddings))
        ]
