import os
from datetime import datetime, timedelta, timezone

import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


load_dotenv()

DB_URL = os.getenv("TIGER_DB_URL")

if not DB_URL:
    raise RuntimeError("TIGER_DB_URL is missing from .env")


EVENTS = [
    {
        "minutes_ago": 720,
        "satellite_id": "SD-OPS-01",
        "event_type": "thermal",
        "severity": "warning",
        "content": (
            "Satellite thermal subsystem reported elevated temperature "
            "near the payload electronics during sustained operation."
        ),
        "metadata": {
            "subsystem": "thermal",
            "payload": "earth-observation",
            "status": "monitoring",
        },
    },
    {
        "minutes_ago": 700,
        "satellite_id": "SD-OPS-01",
        "event_type": "power",
        "severity": "warning",
        "content": (
            "Battery voltage decreased while payload activity remained high "
            "during the observation window."
        ),
        "metadata": {
            "subsystem": "power",
            "payload": "earth-observation",
            "status": "monitoring",
        },
    },
    {
        "minutes_ago": 660,
        "satellite_id": "SD-OPS-01",
        "event_type": "communications",
        "severity": "info",
        "content": (
            "Ground station communication was restored after a temporary "
            "reduction in received signal quality."
        ),
        "metadata": {
            "subsystem": "communications",
            "station": "PAN-GS-01",
            "status": "restored",
        },
    },
    {
        "minutes_ago": 610,
        "satellite_id": "SD-OPS-01",
        "event_type": "adcs",
        "severity": "info",
        "content": (
            "Attitude control maintained the expected pointing mode during "
            "the observation pass."
        ),
        "metadata": {
            "subsystem": "adcs",
            "mode": "nominal",
            "status": "nominal",
        },
    },
    {
        "minutes_ago": 560,
        "satellite_id": "SD-OPS-01",
        "event_type": "payload",
        "severity": "warning",
        "content": (
            "Earth observation payload processing exceeded the expected "
            "CPU utilization range."
        ),
        "metadata": {
            "subsystem": "payload",
            "cpu_state": "elevated",
            "status": "monitoring",
        },
    },
    {
        "minutes_ago": 500,
        "satellite_id": "SD-OPS-01",
        "event_type": "power",
        "severity": "critical",
        "content": (
            "Battery level approached the low-power threshold while the "
            "payload remained enabled."
        ),
        "metadata": {
            "subsystem": "power",
            "battery_state": "low",
            "payload_enabled": True,
        },
    },
    {
        "minutes_ago": 430,
        "satellite_id": "SD-OPS-01",
        "event_type": "thermal",
        "severity": "info",
        "content": (
            "Thermal conditions returned toward the expected operating "
            "range after payload activity decreased."
        ),
        "metadata": {
            "subsystem": "thermal",
            "status": "recovering",
        },
    },
    {
        "minutes_ago": 350,
        "satellite_id": "SD-OPS-01",
        "event_type": "communications",
        "severity": "warning",
        "content": (
            "Telemetry signal strength temporarily dropped during the "
            "ground station contact window."
        ),
        "metadata": {
            "subsystem": "communications",
            "status": "degraded",
        },
    },
    {
        "minutes_ago": 280,
        "satellite_id": "SD-OPS-02",
        "event_type": "thermal",
        "severity": "warning",
        "content": (
            "Payload temperature increased during an imaging sequence, "
            "requiring additional thermal monitoring."
        ),
        "metadata": {
            "subsystem": "thermal",
            "payload": "camera",
            "status": "monitoring",
        },
    },
    {
        "minutes_ago": 210,
        "satellite_id": "SD-OPS-02",
        "event_type": "power",
        "severity": "info",
        "content": (
            "Solar charging increased the available battery energy after "
            "the satellite entered a favorable illumination period."
        ),
        "metadata": {
            "subsystem": "power",
            "charging": True,
            "status": "nominal",
        },
    },
    {
        "minutes_ago": 120,
        "satellite_id": "SD-OPS-02",
        "event_type": "communications",
        "severity": "info",
        "content": (
            "High-quality telemetry was received from the satellite during "
            "a scheduled ground station pass."
        ),
        "metadata": {
            "subsystem": "communications",
            "status": "nominal",
        },
    },
    {
        "minutes_ago": 45,
        "satellite_id": "SD-OPS-02",
        "event_type": "payload",
        "severity": "warning",
        "content": (
            "Payload processing latency increased while several observation "
            "tasks were queued."
        ),
        "metadata": {
            "subsystem": "payload",
            "status": "degraded",
        },
    },
]


def main():
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Connecting to Tiger Cloud...")
    conn = psycopg2.connect(DB_URL)

    sql = """
        INSERT INTO mission_event_embeddings (
            time,
            satellite_id,
            event_type,
            severity,
            content,
            metadata,
            embedding
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s::vector
        )
    """

    now = datetime.now(timezone.utc)

    try:
        with conn.cursor() as cur:
            for event in EVENTS:
                event_time = now - timedelta(
                    minutes=event["minutes_ago"]
                )

                vector = model.encode(
                    event["content"],
                    normalize_embeddings=True,
                )

                vector_text = (
                    "["
                    + ",".join(f"{float(value):.8f}" for value in vector)
                    + "]"
                )

                cur.execute(
                    sql,
                    (
                        event_time,
                        event["satellite_id"],
                        event["event_type"],
                        event["severity"],
                        event["content"],
                        psycopg2.extras.Json(event["metadata"]),
                        vector_text,
                    ),
                )

                print(
                    f"Inserted: {event['satellite_id']} "
                    f"{event['event_type']} "
                    f"{event['severity']}"
                )

        conn.commit()

        print("All embeddings inserted successfully.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
        print("Tiger Cloud connection closed.")


if __name__ == "__main__":
    main()