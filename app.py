import os
import logging
from fastapi import Depends, FastAPI, Form, HTTPException, UploadFile

from src.core.auth import verify_api_key
from src.core.models import UploadPayload, DeleteRequest
from src.services.document_service import DocumentService

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Document Extractor API",
    description="API para processamento e indexação de documentos",
)


@app.post("/upload")
async def upload(
    file: UploadFile,
    filepath: str = Form(None),
    id: str = Form(),
    api_key: str = Depends(verify_api_key),
):
    try:
        if not id:
            logger.warning("Upload sem ID fornecido")
            raise HTTPException(status_code=400, detail="ID é obrigatório")

        if not file:
            logger.warning("Upload sem arquivo")
            raise HTTPException(status_code=400, detail="Arquivo é obrigatório")

        logger.info(f"Upload iniciado: ID={id}, arquivo={file.filename}")
        file_bytes = await file.read()

        payload = UploadPayload(
            id=id,
            filepath=filepath,
            file_bytes=file_bytes,
            filename=file.filename,
            content_type=file.content_type,
        )
        document_service = DocumentService()

        chunk_count = document_service.process_file_upload(payload)
        logger.info(f"Upload concluído: ID={id}, chunks={chunk_count}")

        return {
            "status": "ok",
            "chunks": chunk_count,
            "message": f"Arquivo '{file.filename}' processado com sucesso. {chunk_count} chunks gerados.",
        }
    except HTTPException:
        raise
    except ValueError as ve:
        logger.error(f"Erro de validação no upload: {str(ve)}")
        raise HTTPException(status_code=400, detail=f"Erro de validação: {str(ve)}")
    except Exception as exc:
        logger.error(f"Erro inesperado no upload: {str(exc)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar arquivo: {str(exc)}"
        )


@app.post("/delete")
async def delete_documents(
    request: DeleteRequest,
    api_key: str = Depends(verify_api_key),
):
    try:
        if not request.ids or len(request.ids) == 0:
            logger.warning("Tentativa de delete sem IDs")
            raise HTTPException(
                status_code=400, detail="Lista de IDs não pode estar vazia"
            )

        document_service = DocumentService()

        v_deleted = document_service.delete_vectors_by_ids(request.ids)

        message = f"Deletados com sucesso {v_deleted} vetore(s) correspondente(s) a {len(request.ids)} documento(s)."

        logger.info(f"Delete concluído: {message}")

        return {
            "status": "ok",
            "deleted_count": v_deleted,
            "message": message,
        }
    except HTTPException:
        raise
    except ValueError as ve:
        logger.error(f"Erro de validação na deleção: {str(ve)}")
        raise HTTPException(status_code=400, detail=f"Erro de validação: {str(ve)}")
    except Exception as exc:
        logger.error(f"Erro inesperado na deleção: {str(exc)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Erro ao deletar documentos: {str(exc)}"
        )


@app.get("/health")
async def health_check():
    """Endpoint para verificar se a API está funcionando."""
    return {"status": "healthy", "message": "API está funcionando corretamente"}


@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do Document Extractor!"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8080))
    must_reload = os.environ.get("ENV", "production") == "development"

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=must_reload,
    )
