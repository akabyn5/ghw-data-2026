# Implement AI-Powered Vector Search with pgvector

## Database

Tiger Cloud service:
ghw-data-hypertable

PostgreSQL extension:
pgvector

## Vector dataset

Table:
mission_event_embeddings

Table type:
TimescaleDB hypertable

Vector dimension:
384

Embedding model:
all-MiniLM-L6-v2

## Indexed search

Index:
mission_event_embedding_hnsw

Distance metric:
Cosine distance

Operator:
<=>

## Data

The dataset contains simulated Space Dogs operational events with:

- timestamp
- satellite ID
- event type
- severity
- event content
- JSON metadata
- 384-dimensional embedding

## Search

The Python application generates an embedding for a natural-language query and performs similarity search directly inside Tiger Cloud.

The SQL search combines:

- vector similarity
- time filtering
- metadata filtering

Example semantic query:

"Which recent events are related to high temperature or thermal problems during payload operation?"

## Architecture

Operational event
    ↓
Sentence Transformer
    ↓
384-dimensional embedding
    ↓
Tiger Cloud / PostgreSQL
    ↓
TimescaleDB hypertable
    ↓
pgvector HNSW index
    ↓
Similarity + time + metadata search

## Evidence

Screenshots:

- pgvector-extension.png
- vector-dimensions.png
- vector-records.png
- vector-search-results.png
- hybrid-time-metadata-search.png

Repository:

https://github.com/akabyn5/ghw-data-2026