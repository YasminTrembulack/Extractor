import os

from dotenv import load_dotenv
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

load_dotenv()

api_key_header = APIKeyHeader(name="x-api-key")

API_KEY = os.environ["EXTRACTOR_API_KEY"]


def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="API Key inválida")
