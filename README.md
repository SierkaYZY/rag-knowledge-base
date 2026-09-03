# RAG Knowledge Base

A modular Retrieval-Augmented Generation (RAG) knowledge-base QA system built with Python, BGE embeddings, ChromaDB, DeepSeek API, and FastAPI.

The project implements the core RAG pipeline from document indexing to HTTP-based question answering without relying on a high-level RAG framework.

## Features

- Sentence-aware text chunking
- Sentence-level chunk overlap
- Long-sentence fallback splitting
- BGE-based text embeddings
- Persistent ChromaDB vector storage
- Top-K semantic retrieval
- Experimental distance-based relevance filtering
- Guard Clause for insufficient retrieval results
- Grounded prompt construction
- Source citation with document metadata
- FastAPI `/health` and `/ask` endpoints
- Auto-generated Swagger API documentation

## Architecture

```text
Document
   ↓
Document Loading
   ↓
Sentence-aware Chunking
   ↓
BGE Embedding
   ↓
ChromaDB
   ↓
Query Embedding
   ↓
Top-K Retrieval
   ↓
Distance Filtering
   ↓
Guard Clause
   ↓
Context + Source Metadata
   ↓
Grounded Prompt
   ↓
DeepSeek
   ↓
Answer + Citation
   ↓
FastAPI JSON Response
```

## Project Structure

```text
rag-knowledge-base/
├── api/
│   ├── __init__.py
│   └── main.py
│
├── data/
│   └── sample/
│       └── sample.txt
│
├── data_structures/
├── embedding/
├── file_io/
├── function/
├── llm/
├── rag_pipeline/
├── retrieval/
├── text_splitter/
├── vector_store/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Key Engineering Improvements

### 1. Sentence-aware Chunking

The initial implementation used fixed character-based splitting, which could break words and semantic boundaries.

The chunking pipeline was improved to:

- detect Chinese and English sentence boundaries;
- group complete sentences into chunks;
- preserve sentence-level overlap;
- split oversized sentences at word boundaries when possible;
- fall back to character-level splitting only when necessary.

During testing, a control-flow bug was also identified in the long-sentence processing logic. When the current sentence buffer was empty, some standalone long sentences could be skipped before being added to the chunk list.

The issue was located by tracing data across module boundaries:

```text
sample.txt
   ↓
load_txt()
   ↓
split_sentences()
   ↓
group_sentences()
   ↓
split_long_sentence()
```

After correcting the control flow, all source content could be preserved during chunk generation.

### 2. Retrieval Relevance Filtering

Top-K vector retrieval returns the closest results in the knowledge base, but this does not guarantee that every returned chunk is sufficiently relevant to the user query.

An experimental distance-based filtering stage was added before prompt construction to reduce low-relevance context.

The current threshold should be treated as a heuristic rather than a universal relevance boundary, because retrieval distance is affected by factors such as:

- embedding model;
- chunking strategy;
- corpus distribution;
- query distribution.

### 3. Guard Clause

If no retrieved document satisfies the current relevance condition, the pipeline returns early instead of unnecessarily calling the LLM.

This helps reduce:

- unnecessary API calls;
- token consumption;
- response latency;
- unsupported generation risk.

### 4. Prompt Grounding

The generation prompt explicitly requires the language model to answer according to the retrieved reference materials.

If the available materials are insufficient, the model is instructed to state that the answer cannot be supported by the current knowledge base rather than freely supplementing information from outside the provided context.

### 5. Source Citation

Retrieved document metadata is propagated into the context so that each reference can be identified using a source number.

Example:

```text
[资料1]
Source file: sample.txt
Chunk ID: 0
Content: ...
```

The prompt then requires factual statements and conclusions to cite the corresponding source identifier, such as:

```text
[资料1]
[资料2]
```

This improves answer traceability and makes it easier to verify which retrieved chunk supports a generated statement.

### 6. FastAPI Service

The original RAG pipeline was executed as a local Python workflow.

FastAPI is now used to expose the RAG system as an HTTP service so that external clients can call the question-answering pipeline.

Available endpoints:

```text
GET  /health
POST /ask
```

The API is served with Uvicorn and automatically documented through Swagger UI.

## Example

### Request

```json
{
  "question": "How can RAG help language models?"
}
```

### Response

```json
{
  "question": "How can RAG help language models?",
  "answer": "RAG can help language models answer questions based on external knowledge sources and reduce unsupported generation when appropriate retrieval and grounding mechanisms are used. [资料1]"
}
```

## Installation

Clone the repository:

```bash
git clone https://github.com/SierkaYZY/rag-knowledge-base.git
cd rag-knowledge-base
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file based on `.env.example`:

```text
DEEPSEEK_API_KEY=your_deepseek_api_key
```

Do not commit the real `.env` file or API key to Git.

## Build the Knowledge Base

A small demo document is provided under:

```text
data/sample/sample.txt
```

Run:

```bash
python -m rag_pipeline.index_document
```

The pipeline will:

```text
Load document
   ↓
Build document metadata
   ↓
Split document into chunks
   ↓
Generate BGE embeddings
   ↓
Store chunks and embeddings in ChromaDB
```

The local ChromaDB database will be generated under:

```text
./chroma_db
```

The database directory is excluded from Git and can be rebuilt from the source document.

## Run the API

Start the FastAPI application with Uvicorn:

```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

The Swagger UI can be used to test the `/ask` endpoint directly.

## RAG Query Flow

```text
User Question
   ↓
FastAPI POST /ask
   ↓
Query Embedding
   ↓
ChromaDB Top-K Retrieval
   ↓
Distance-based Filtering
   ↓
Guard Clause
   ↓
Context Construction
   ↓
Source Metadata Formatting
   ↓
Grounded Prompt
   ↓
DeepSeek API
   ↓
Answer + Source Citation
   ↓
JSON Response
```

## Tech Stack

- Python 3.11
- FastAPI
- Uvicorn
- Pydantic
- Sentence Transformers
- BAAI/bge-small-zh-v1.5
- ChromaDB
- DeepSeek API
- python-dotenv

## Current Direct Dependencies

```text
fastapi==0.141.1
uvicorn==0.52.4
pydantic==2.13.4
sentence-transformers==6.0.0
chromadb==1.5.9
openai==3.6.0
python-dotenv==1.2.3
```

## Known Limitations

- The current demo mainly supports TXT document ingestion.
- Retrieval relevance filtering currently uses a heuristic distance threshold.
- A fixed distance threshold cannot reliably separate all relevant and irrelevant chunks across different corpora.
- Retrieval quality is sensitive to the embedding model, chunking strategy, corpus, and query distribution.
- A systematic retrieval evaluation dataset has not yet been established.
- No reranker is currently used.
- Citation currently operates mainly at filename/chunk level rather than page-level document citation.
- Prompt grounding and source citation can reduce unsupported generation risk but cannot guarantee complete factual correctness.
- The current implementation focuses on a local development workflow and has not yet been containerized or deployed as a production service.

## Planned Improvements

- Build a labeled retrieval evaluation dataset
- Evaluate different embedding and retrieval strategies
- Introduce a reranking stage
- Make retrieval parameters configurable
- Support additional document formats
- Improve citation granularity
- Add more structured API error handling
- Containerize the application with Docker
- Explore production deployment

## Security

Sensitive credentials must not be committed to the repository.

The following files and generated data are excluded through `.gitignore`:

```text
.env
chroma_db/
chroma.db/
__pycache__/
*.pyc
.vscode/
```

Use `.env.example` as the configuration template and store the real DeepSeek API key only in your local `.env` file.