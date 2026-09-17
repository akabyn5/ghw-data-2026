# Accelerate Dashboards with Continuous Aggregates

**Challenge:** Accelerate Dashboards with Continuous Aggregates  
**Event:** MLH Global Hack Week: Data 2026  
**Status:** ✅ Completed

## Overview

This project demonstrates the creation of a **Continuous Aggregate (CAGG)** on a TimescaleDB hypertable to pre-compute real-time metrics. Continuous Aggregates significantly improve dashboard performance by calculating complex analytical queries in the background, delivering fast response times while reducing load on the primary database.

## What We Built

### Service
- **Service Name:** `ghw-data-space-dogs`
- **Type:** TimescaleDB (Tiger Cloud)

### Continuous Aggregate
- **Name:** `conditions_hourly`
- **Source Hypertable:** `conditions`
- **Aggregation Interval:** 1 hour

The continuous aggregate computes the following metrics per device and time bucket:

| Metric            | Description                     |
|-------------------|---------------------------------|
| avg_temperature   | Average temperature             |
| min_temperature   | Minimum temperature             |
| max_temperature   | Maximum temperature             |
| avg_humidity      | Average humidity                |
| min_humidity      | Minimum humidity                |
| max_humidity      | Maximum humidity                |
| reading_count     | Number of readings in the bucket|

### Sample Query Results

```sql
SELECT
  bucket,
  device,
  ROUND(avg_temperature::numeric, 2) AS avg_temperature,
  ROUND(min_temperature::numeric, 2) AS min_temperature,
  ROUND(max_temperature::numeric, 2) AS max_temperature,
  ROUND(avg_humidity::numeric, 2) AS avg_humidity,
  ROUND(min_humidity::numeric, 2) AS min_humidity,
  ROUND(max_humidity::numeric, 2) AS max_humidity,
  reading_count
FROM conditions_hourly
ORDER BY bucket DESC, device;
Results:

















































bucketdeviceavg_temperaturemin_temperaturemax_temperatureavg_humiditymin_humiditymax_humidityreading_count2026-09-17 14:00:00+00sensor-122.2022.2022.2045.1045.1045.1012026-09-17 13:00:00+00sensor-122.3022.3022.3044.8044.8044.8012026-09-17 12:00:00+00sensor-122.1022.1022.1045.0045.0045.001
Filtered Query Example
SQLSELECT
  bucket,
  device,
  ROUND(avg_temperature::numeric, 2) AS avg_temperature,
  ROUND(avg_humidity::numeric, 2) AS avg_humidity,
  reading_count
FROM conditions_hourly
WHERE device = 'sensor-1'
ORDER BY bucket DESC;
Why Continuous Aggregates Matter

Pre-computes expensive aggregations in the background
Enables fast dashboard queries without scanning the full hypertable
Supports real-time and historical analysis
Reduces computational load on the primary database

Screenshots

SQL Editor showing successful query on conditions_hourly
Aggregated results with temperature and humidity metrics
Device-filtered query results


Team: Global Hack Week – Data

Date: September 2026