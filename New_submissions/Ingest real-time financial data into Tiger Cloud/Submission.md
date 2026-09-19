# Ingest real-time financial data into Tiger Cloud

## Pipeline

Twelve Data WebSocket → Python ingestion pipeline → Tiger Cloud TimescaleDB hypertable.

## Source

Twelve Data real-time financial WebSocket stream.

Symbols used:

* BTC/USD
* ETH/USD

## Processing

The Python pipeline:

1. Connects to Twelve Data using the official Python client.
2. Subscribes to cryptocurrency price streams.
3. Receives real-time price events.
4. Converts timestamps and numeric fields to the database schema.
5. Accumulates records in an in-memory batch.
6. Inserts batches into Tiger Cloud using psycopg2.
7. Stores the records in the `crypto_ticks` TimescaleDB hypertable.

## Tiger Cloud database

Service:

`ghw-data-hypertable`

Hypertable:

`crypto_ticks`

Columns:

* `time`
* `symbol`
* `price`
* `day_volume`

Relational metadata table:

`crypto_assets`

## Analytics

Created Continuous Aggregate:

`one_day_candle`

The aggregate produces:

* Open
* High
* Low
* Close
* Day volume

## Verification

The pipeline was verified by querying the `crypto_ticks` hypertable and confirming that real-time BTC/USD and ETH/USD records were inserted into Tiger Cloud.

The OHLCV Continuous Aggregate was also queried successfully.

## Evidence

* `Screenshots/websocket-stream.png`
* `Screenshots/tiger-ingested-data.png`
* `Screenshots/ohlcv-cagg.png`

## Repository

https://github.com/akabyn5/ghw-data-2026
