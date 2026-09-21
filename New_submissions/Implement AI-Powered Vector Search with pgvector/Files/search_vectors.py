import os

import psycopg2
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


load_dotenv()

DB_URL = os.getenv("TIGER_DB_URL")

if not DB_URL:
    raise RuntimeError("TIGER_DB_URL is missing from .env")


MODEL_NAME = "all-MiniLM-L6-v2"


def main():
    query_text = (
        "Find events where the spacecraft was experiencing "
        "low battery or power-related problems."
        )

    print("=" * 70)
    print("Space Dogs ARPIP - pgvector semantic search")
    print("=" * 70)
    print()
    print(f"Query: {query_text}")
    print()
    print(f"Loading embedding model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    query_vector = model.encode(
        query_text,
        normalize_embeddings=True,
    )

    vector_text = (
        "["
        + ",".join(f"{float(value):.8f}" for value in query_vector)
        + "]"
    )

    print(f"Embedding dimensions: {len(query_vector)}")
    print("Connecting to Tiger Cloud...")

    conn = psycopg2.connect(DB_URL)

    sql ="""
        WITH query_embedding AS (
            SELECT %s::vector AS embedding
        )
        SELECT
            m.time,
            m.satellite_id,
            m.event_type,
            m.severity,
            m.content,
            1 - (m.embedding <=> q.embedding) AS similarity
        FROM mission_event_embeddings AS m
        CROSS JOIN query_embedding AS q
        WHERE m.time >= NOW() - INTERVAL '24 hours'
          AND m.event_type = 'power'
        ORDER BY m.embedding <=> q.embedding
        LIMIT 5;
    """

    try:
        with conn.cursor() as cur:
            cur.execute(sql, (vector_text,))
            rows = cur.fetchall()

        print()
        print("Search results:")
        print("-" * 70)

        if not rows:
            print("No matching records found.")
            print()
            print("Check that mission_event_embeddings contains data")
            print("from the last 24 hours.")
            return

        for row in rows:
            (
                timestamp,
                satellite_id,
                event_type,
                severity,
                content,
                similarity,
            ) = row

            print()
            print(f"Time:       {timestamp}")
            print(f"Satellite:  {satellite_id}")
            print(f"Event:      {event_type}")
            print(f"Severity:   {severity}")
            print(f"Similarity: {float(similarity):.4f}")
            print(f"Content:    {content}")

        print()
        print("-" * 70)
        print(f"Returned {len(rows)} result(s).")

    finally:
        conn.close()

    print()
    print("Tiger Cloud connection closed.")


if __name__ == "__main__":
    main()