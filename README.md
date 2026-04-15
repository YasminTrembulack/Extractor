# Backend do Sistema de Processamento de Documentos

Sistema FastAPI para processamento de documentos com extração de texto, chunking, geração de embeddings e indexação no Pinecone.

## Estrutura do Projeto

```
backend/
├── app.py                 # Ponto de entrada da aplicação FastAPI
├── requirements.txt       # Dependências Python
├── .env                   # Variáveis de ambiente
├── src/                   # Código fonte organizado
│   ├── core/              # Configurações e utilitários
│   │   ├── __init__.py
│   │   └── config.py      # Classe Config para centralizar configurações
│   ├── services/          # Lógica de negócio e integrações
│   │   ├── __init__.py
│   │   ├── document_service.py  # Classe DocumentProcessor
│   │   └── pinecone_service.py  # Classe VectorService
│   ├── processing/        # Processamento de texto e embeddings
│   │   ├── __init__.py
│   │   ├── chunking.py    # Classe TextChunker
│   │   └── embeddings.py  # Classe EmbeddingService
│   └── extractors/        # Extração de texto de diferentes formatos
│       ├── __init__.py
│       ├── pdf.py         # Extração de PDF
│       ├── text.py        # Extração de texto simples
│       └── word.py        # Extração de .docx e .doc
├── chunking.py           # Arquivo antigo (removido)
├── embeddings.py         # Arquivo antigo (removido)
├── core/                 # Pasta antiga (movida para src/)
├── services/             # Pasta antiga (movida para src/)
├── extractors/           # Pasta antiga (movida para src/)
└── processing/           # Pasta antiga (movida para src/)
```

## Funcionalidades

- **Upload de arquivos**: Suporte para PDF, TXT, DOCX
- **Extração de texto**: Extração automática baseada no tipo de arquivo
- **Chunking**: Divisão inteligente do texto em chunks
- **Embeddings**: Geração de embeddings usando Sentence Transformers
- **Indexação**: Armazenamento no Pinecone com metadados
- **Atualização**: Substituição automática de documentos existentes

## Arquitetura

### Classes Principais

- **Config**: Centraliza todas as configurações da aplicação
- **DocumentProcessor**: Orquestra o processamento completo de documentos
- **VectorService**: Gerencia operações com o Pinecone
- **TextChunker**: Divide texto em chunks menores
- **EmbeddingService**: Gera embeddings vetoriais

### Fluxo de Processamento

1. Upload do arquivo via endpoint `/upload`
2. Seleção do extractor baseado no MIME type ou extensão
3. Extração do texto do arquivo
4. Divisão do texto em chunks
5. Geração de embeddings para cada chunk
6. Construção dos vetores para indexação
7. Upsert no Pinecone (com deleção prévia se documento existir)

## Como Executar

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente no .env
PINECONE_API_KEY=your_api_key
PINECONE_INDEX_NAME=your_index_name

# Executar aplicação
python app.py
```

## API

### POST /upload

Upload de arquivo para processamento.

**Parâmetros:**

- `file`: Arquivo multipart

**Resposta:**

```json
{
  "status": "ok",
  "chunks": 15
}
```

## Formatos Suportados

- **PDF** (.pdf): Extração completa de texto
- **Texto** (.txt): Leitura direta
- **Word** (.docx): Extração via python-docx
- **Word antigo** (.doc): Mensagem orientando conversão para .docx

## Configuração

Variáveis de ambiente necessárias:

- `PINECONE_API_KEY`: Chave da API do Pinecone
- `PINECONE_INDEX_NAME`: Nome do índice (opcional, padrão: "default-index")
- `PINECONE_CLOUD`: Cloud provider (opcional, padrão: "aws")
- `PINECONE_REGION`: Região (opcional, padrão: "us-east-1")
