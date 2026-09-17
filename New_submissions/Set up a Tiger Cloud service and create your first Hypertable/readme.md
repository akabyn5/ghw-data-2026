# Tiger Cloud Hypertable Setup

**Challenge:** Set up a Tiger Cloud service and create your first Hypertable  
**Event:** MLH Global Hack Week: Data 2026  
**Status:** ✅ Completed

## Overview

This project demonstrates the creation of a Tiger Cloud service and the setup of a **hypertable** using TimescaleDB.  

A hypertable is the core abstraction in TimescaleDB for time-series data. It behaves like a regular PostgreSQL table (supporting standard SQL operations), but automatically partitions data by time into chunks. This design allows efficient querying of large time-series datasets.

## What We Built

### 1. Tiger Cloud Service
- **Service Name:** `ghw-data-hypertable`
- **Type:** TimescaleDB
- **Status:** Ready
- **Region:** US East (N. Virginia)
- **Compute:** 0.5 CPU / 2 GiB Memory

### 2. Hypertable: `conditions`

| Column       | Type                |
|--------------|---------------------|
| time         | TIMESTAMPTZ         |
| location     | TEXT                |
| device       | TEXT                |
| temperature  | DOUBLE PRECISION    |
| humidity     | DOUBLE PRECISION    |

**Hypertable Configuration:**
- Created with `tsdb.hypertable`
- `tsdb.segmentby = 'device'`
- `tsdb.orderby = 'time DESC'`

### 3. Sample Data
Three sensor records were inserted into the `conditions` hypertable:

| time                          | location | device   | temperature | humidity |
|-------------------------------|----------|----------|-------------|----------|
| 2026-09-17 14:20:19.028747+00 | office   | sensor-1 | 22.2        | 45.1     |
| 2026-09-17 13:20:19.028747+00 | office   | sensor-1 | 22.3        | 44.8     |
| 2026-09-17 12:20:19.028747+00 | office   | sensor-1 | 22.1        | 45.0     |

### 4. Verification
The hypertable was confirmed using:

```sql
SELECT hypertable_schema, hypertable_name
FROM timescaledb_information.hypertables
WHERE hypertable_name = 'conditions';
Result: public.conditions
Key Queries Used
SQL-- View latest sensor readings
SELECT *
FROM conditions
ORDER BY time DESC;

-- Confirm hypertable registration
SELECT hypertable_schema, hypertable_name
FROM timescaledb_information.hypertables
WHERE hypertable_name = 'conditions';
Screenshots

Service overview showing ghw-data-hypertable and ghw-data-space-dogs
SQL Editor with successful query on the conditions hypertable
Verification query confirming the hypertable exists


Team: Global Hack Week – Data

Date: September 2026