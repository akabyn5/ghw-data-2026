```markdown
# Ingest Real-Time Financial Data into Tiger Cloud

**Challenge:** Ingest real-time financial data into Tiger Cloud  
**Event:** MLH Global Hack Week: Data 2026  
**Status:** ✅ Completed

## Overview

This project implements a complete real-time data pipeline that streams live financial market data from Twelve Data into a Tiger Cloud TimescaleDB service. The pipeline ingests cryptocurrency price ticks, stores them in a hypertable, and materializes daily OHLCV candles using a Continuous Aggregate for fast analytical queries.

## Architecture

```
Twelve Data WebSocket
        ↓
Python Ingestion Pipeline
        ↓
Batch INSERT (psycopg2)
        ↓
Tiger Cloud (TimescaleDB)
        ├── crypto_ticks          (Hypertable)
        └── one_day_candle        (Continuous Aggregate)
```

## Tiger Cloud Service

- **Service Name:** `ghw-data-hypertable`
- **Type:** TimescaleDB

## Database Schema

### 1. `crypto_ticks` (Hypertable)

| Column       | Type              | Description                  |
|--------------|-------------------|------------------------------|
| time         | TIMESTAMPTZ       | Timestamp of the price tick  |
| symbol       | TEXT              | Trading pair (e.g. BTC/USD)  |
| price        | DOUBLE PRECISION  | Current price                |
| day_volume   | NUMERIC           | Day volume                   |

**Hypertable Configuration:**
- `tsdb.segmentby = 'symbol'`
- `tsdb.orderby = 'time DESC'`

### 2. `crypto_assets` (Relational Metadata)

| Column  | Type | Description                |
|---------|------|----------------------------|
| symbol  | TEXT | Unique trading pair symbol |
| name    | TEXT | Human-readable asset name  |

**Populated Assets:**
- `BTC/USD` → Bitcoin / US Dollar
- `ETH/USD` → Ethereum / US Dollar

### 3. `one_day_candle` (Continuous Aggregate)

Daily OHLCV candles generated from the raw tick stream:

| Column     | Description              |
|------------|--------------------------|
| bucket     | 1-day time bucket        |
| symbol     | Trading pair             |
| open       | Opening price            |
| high       | Highest price            |
| low        | Lowest price             |
| close      | Closing price            |
| day_volume | Last day volume          |

## Pipeline Details

### Data Source
- **Provider:** Twelve Data
- **Protocol:** WebSocket
- **Symbols:** `BTC/USD`, `ETH/USD`
- **Event Type:** Real-time `price` events

### Ingestion Logic
1. Connect to Twelve Data WebSocket using the official Python client
2. Subscribe to BTC/USD and ETH/USD
3. Receive and validate price events
4. Convert timestamps to UTC and numeric fields to the correct types
5. Accumulate records in an in-memory batch (size = 20)
6. Perform efficient batch inserts into `crypto_ticks` using `psycopg2.extras.execute_values`
7. Continuously stream data until manually stopped

### Key Technologies
- Python 3
- Twelve Data Python Client (`twelvedata`)
- WebSocket
- `psycopg2` / `psycopg2-binary`
- `python-dotenv`
- Tiger Cloud / TimescaleDB
- Hypertables
- Continuous Aggregates

## Verification Queries

### Confirm ingested ticks
```sql
SELECT
    COUNT(*) AS total_ticks,
    COUNT(DISTINCT symbol) AS symbols,
    MIN(time) AS first_tick,
    MAX(time) AS last_tick
FROM crypto_ticks;
```

### Latest price ticks
```sql
SELECT time, symbol, price, day_volume
FROM crypto_ticks
ORDER BY time DESC
LIMIT 20;
```

### Per-symbol summary
```sql
SELECT
    symbol,
    COUNT(*) AS ticks,
    MIN(time) AS first_tick,
    MAX(time) AS last_tick,
    MIN(price) AS minimum_price,
    MAX(price) AS maximum_price
FROM crypto_ticks
GROUP BY symbol
ORDER BY symbol;
```

### Join with asset metadata
```sql
SELECT
    a.symbol,
    a.name,
    COUNT(t.symbol) AS tick_count,
    MAX(t.time) AS latest_tick
FROM crypto_assets AS a
LEFT JOIN crypto_ticks AS t
    ON t.symbol = a.symbol
GROUP BY a.symbol, a.name
ORDER BY a.symbol;
```

### Query daily OHLCV candles
```sql
SELECT
    bucket,
    symbol,
    "open",
    high,
    low,
    "close",
    day_volume
FROM one_day_candle
WHERE symbol = 'BTC/USD'
ORDER BY bucket;
```

## Evidence

- Real-time WebSocket stream connected and receiving price events
- Successful batch inserts into Tiger Cloud (`[Tiger Cloud] Batch insert #N completed`)
- Live rows present in the `crypto_ticks` hypertable
- Daily OHLCV Continuous Aggregate (`one_day_candle`) created and queryable

## Repository

Source code and supporting files are available in the project repository under the challenge folder.

---

**Team:** Global Hack Week – Data (Space Dogs)  
**Date:** September 2026
```