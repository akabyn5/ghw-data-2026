```markdown
# Implement AI-Powered Vector Search with pgvector

**Challenge:** Implement AI-Powered Vector Search with pgvector  
**Event:** MLH Global Hack Week: Data 2026  
**Status:** ✅ Completed

## Overview

This project implements AI-powered semantic search over operational event data using **pgvector** inside a Tiger Cloud TimescaleDB service. Natural-language queries are converted into embeddings and matched against stored event embeddings using cosine similarity, with additional time and metadata filters for hybrid search.

## Tiger Cloud Service

- **Service Name:** `ghw-data-hypertable`
- **PostgreSQL Extension:** `pgvector`

## Vector Dataset

### Table: `mission_event_embeddings`

| Property          | Value                          |
|-------------------|--------------------------------|
| Table Type        | TimescaleDB Hypertable         |
| Vector Dimension  | 384                            |
| Embedding Model   | `all-MiniLM-L6-v2`             |

### Data Contents

Each record represents a simulated Space Dogs operational event and includes:

- Timestamp
- Satellite ID
- Event type
- Severity
- Event content (text)
- JSON metadata
- 384-dimensional embedding vector

## Vector Index

| Property        | Value                          |
|-----------------|--------------------------------|
| Index Name      | `mission_event_embedding_hnsw` |
| Index Type      | HNSW                           |
| Distance Metric | Cosine distance                |
| Operator        | `<=>`                          |

## Search Architecture

```
Operational event
        ↓
Sentence Transformer (all-MiniLM-L6-v2)
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
```

### How Search Works

1. A natural-language query is converted into a 384-dimensional embedding using the same Sentence Transformer model.
2. The embedding is sent to Tiger Cloud.
3. A similarity search is performed using the HNSW index and cosine distance (`<=>`).
4. Results can be further filtered by time range and metadata fields for hybrid search.

### Example Semantic Query

> “Which recent events are related to high temperature or thermal problems during payload operation?”

## Key Features

- Semantic (vector) search over operational event text
- Hybrid filtering by time and metadata
- Efficient approximate nearest-neighbor search via HNSW
- Full integration with TimescaleDB hypertables on Tiger Cloud

## Evidence

- `pgvector-extension.png` – Confirmation that the pgvector extension is enabled
- `vector-dimensions.png` – Verification of 384-dimensional embeddings
- `vector-records.png` – Sample records stored in the hypertable
- `vector-search-results.png` – Results of a pure similarity search
- `hybrid-time-metadata-search.png` – Hybrid search combining vector similarity, time, and metadata filters

## Repository

https://github.com/akabyn5/ghw-data-2026

---

**Team:** Global Hack Week – Data (Space Dogs)  
**Date:** September 2026
```