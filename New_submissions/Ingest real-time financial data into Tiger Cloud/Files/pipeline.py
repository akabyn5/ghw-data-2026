import os
import time
from datetime import datetime, timezone

import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from twelvedata import TDClient


load_dotenv()

TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")
TIGER_DB_URL = os.getenv("TIGER_DB_URL")

if not TWELVE_DATA_API_KEY:
    raise RuntimeError("TWELVE_DATA_API_KEY is missing from .env")

if not TIGER_DB_URL:
    raise RuntimeError("TIGER_DB_URL is missing from .env")


class WebsocketPipeline:
    DB_TABLE = "crypto_ticks"
    DB_COLUMNS = ["time", "symbol", "price", "day_volume"]

    # The guide uses 100.
    # We use 20 here so the hackathon evidence appears quickly.
    MAX_BATCH_SIZE = 20

    def __init__(self, conn):
        self.conn = conn
        self.current_batch = []
        self.insert_counter = 0

    def _insert_values(self, data):
        if not data:
            return

        sql = f"""
            INSERT INTO {self.DB_TABLE}
            ({",".join(self.DB_COLUMNS)})
            VALUES %s
        """

        try:
            with self.conn.cursor() as cursor:
                execute_values(cursor, sql, data)

            self.conn.commit()

            self.insert_counter += 1

            print(
                f"[Tiger Cloud] Batch insert #{self.insert_counter} "
                f"completed: {len(data)} rows"
            )

        except Exception as exc:
            self.conn.rollback()
            print(f"[Tiger Cloud] INSERT FAILED: {exc}")

    def _on_event(self, event):
        event_type = event.get("event")

        # Ignore metadata/heartbeat events.
        if event_type != "price":
            if event_type in {"subscribe-status", "heartbeat"}:
                print(f"[Twelve Data] {event}")
            return

        try:
            timestamp = datetime.fromtimestamp(
                int(event["timestamp"]),
                tz=timezone.utc,
            )

            symbol = event["symbol"]
            price = float(event["price"])

            day_volume = event.get("day_volume")

            if day_volume is not None:
                day_volume = float(day_volume)

            row = (
                timestamp,
                symbol,
                price,
                day_volume,
            )

            self.current_batch.append(row)

            print(
                f"[PRICE] {symbol} "
                f"{price} "
                f"UTC={timestamp.isoformat()} "
                f"batch={len(self.current_batch)}/{self.MAX_BATCH_SIZE}"
            )

            if len(self.current_batch) >= self.MAX_BATCH_SIZE:
                self._insert_values(self.current_batch)
                self.current_batch = []

        except (KeyError, TypeError, ValueError) as exc:
            print(f"[Twelve Data] Invalid price event: {exc}")
            print(event)

    def flush(self):
        if self.current_batch:
            print(
                f"[Tiger Cloud] Flushing final batch: "
                f"{len(self.current_batch)} rows"
            )

            self._insert_values(self.current_batch)
            self.current_batch = []

    def start(self, symbols):
        td = TDClient(apikey=TWELVE_DATA_API_KEY)

        ws = td.websocket(
            on_event=self._on_event
        )

        print("[Pipeline] Subscribing to:")
        print(", ".join(symbols))

        ws.subscribe(symbols)

        print("[Pipeline] Connecting to Twelve Data WebSocket...")

        ws.connect()

        try:
            while True:
                ws.heartbeat()
                time.sleep(10)

        except KeyboardInterrupt:
            print("\n[Pipeline] Stopping...")

        finally:
            self.flush()

            try:
                ws.disconnect()
            except Exception:
                pass


def main():
    print("======================================")
    print("Space Dogs - GHW Data Financial Pipeline")
    print("Twelve Data -> Tiger Cloud")
    print("======================================")

    conn = psycopg2.connect(TIGER_DB_URL)

    print("[Tiger Cloud] Database connection: OK")

    symbols = [
        "BTC/USD",
        "ETH/USD",
    ]

    pipeline = WebsocketPipeline(conn)

    try:
        pipeline.start(symbols)

    finally:
        pipeline.flush()
        conn.close()
        print("[Tiger Cloud] Database connection closed")


if __name__ == "__main__":
    main()