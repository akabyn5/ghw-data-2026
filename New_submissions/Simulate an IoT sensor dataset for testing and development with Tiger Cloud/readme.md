# Simulate an IoT Sensor Dataset with Tiger Cloud

**Challenge:** Simulate an IoT sensor dataset for testing and development with Tiger Cloud  
**Event:** MLH Global Hack Week: Data 2026  
**Status:** ✅ Completed

## Overview

This project simulates a realistic IoT sensor dataset inside a Tiger Cloud TimescaleDB service. The dataset models multiple sensors collecting time-series environmental and system metrics (temperature and CPU usage), which is ideal for testing analytics, continuous aggregates, and dashboard queries.

## Tiger Cloud Service

- **Service Name:** `ghw-data-space-dogs`  
- **Type:** TimescaleDB  
- **Region:** US East (N. Virginia)

## Tables Created

### 1. `sensors`
Stores metadata for the simulated devices.

| Column     | Description                  |
|------------|------------------------------|
| sensor_id  | Unique sensor identifier     |
| type       | Sensor type                  |
| location   | Physical location            |

**Data:** 4 simulated sensors with type and location metadata.

### 2. `sensor_data` (Hypertable)
Time-series hypertable containing the actual sensor readings.

| Column      | Type              | Description                |
|-------------|-------------------|----------------------------|
| time        | TIMESTAMPTZ       | Timestamp of the reading   |
| sensor_id   | Integer / Text    | Reference to sensors table |
| temperature | Double Precision  | Temperature reading        |
| cpu         | Double Precision  | CPU utilization            |

**Hypertable Configuration:**
- Partitioning column: `time`

## Simulation Details

- **Duration:** 24 hours of simulated data  
- **Interval:** 5-minute readings  
- **Number of sensors:** 4  
- **Approximate volume:** ~1,156 sensor readings  

## Key Queries Demonstrated

### Latest Sensor Readings
```sql
SELECT
  time,
  sensor_id,
  ROUND(temperature::numeric, 2) AS temperature,
  ROUND(cpu::numeric, 4) AS cpu
FROM sensor_data
ORDER BY time DESC
LIMIT 20;
30-Minute Aggregations
SQLSELECT
  period,
  AVG(temperature) AS avg_temp,
  last(temperature, time) AS last_temp,
  AVG(cpu) AS avg_cpu
FROM sensor_data
GROUP BY period
ORDER BY period DESC
LIMIT 20;
Continuous Aggregate Query (conditions_hourly)
SQLSELECT
  bucket,
  device,
  ROUND(avg_temperature::numeric, 2) AS avg_temperature,
  ROUND(avg_humidity::numeric, 2) AS avg_humidity,
  reading_count
FROM conditions_hourly
WHERE device = 'sensor-1'
ORDER BY bucket DESC;
Results Highlights

Successfully generated and inserted multi-sensor time-series data
Confirmed sensor_data is registered as a hypertable
Ran analytical queries for average temperature, last temperature, and CPU usage
Demonstrated time-bucketed aggregations suitable for dashboards

Screenshots

SQL Editor showing raw sensor_data readings
Aggregation queries with avg_temp, last_temp, and avg_cpu
Continuous aggregate results from conditions_hourly


Team: Global Hack Week – Data

Date: September 2026