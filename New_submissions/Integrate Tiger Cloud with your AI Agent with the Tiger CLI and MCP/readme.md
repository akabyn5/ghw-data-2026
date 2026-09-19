# Tiger Cloud + AI Agent Integration (Tiger CLI & MCP)

**Challenge:** Integrate Tiger Cloud with your AI Agent using the Tiger CLI and MCP  
**Event:** MLH Global Hack Week: Data 2026  
**Status:** ✅ Completed

## Overview

This project demonstrates the successful integration of **Tiger Cloud** with an AI agent using the **Tiger CLI** and **Tiger MCP** (Model Context Protocol).

Tiger MCP allows an AI agent to manage Tiger Cloud services and query data using natural language. It is built directly into the Tiger CLI binary and includes tools for service management, SQL execution, and built-in skills such as schema design, hypertable setup, and migration planning. It is also connected to up-to-date Tiger Data documentation.

## What We Built / Completed

- Created a new Tiger Cloud project
- Provisioned a TimescaleDB service named **`ghw-data-space-dogs`**
- Successfully connected and verified the service is **Ready**
- Integrated the service with an AI agent via Tiger CLI + Tiger MCP

### Service Details

| Property              | Value                          |
|-----------------------|--------------------------------|
| Service Name          | `ghw-data-space-dogs`          |
| Environment           | `#dev`                         |
| Type                  | TimescaleDB                    |
| Status                | Ready                          |
| Compute               | 0.5 CPU / 2 GiB Memory         |
| Region                | US East (N. Virginia)          |
| High Availability     | No replica                     |
| Service ID            | `tck6ax8b1j`                   |
| Project ID            | `j6cabsx25t`                   |

## Dashboard Screenshot

The service is live and visible in the Tiger Cloud dashboard under the project **New Project**.

## How It Works

1. Install and authenticate with the **Tiger CLI**
2. Enable / use the built-in **Tiger MCP** server
3. Connect an AI agent (e.g., Claude, Cursor, or other MCP-compatible clients)
4. The agent can now:
   - List and manage Tiger Cloud services
   - Run SQL queries against the database
   - Design schemas and hypertables
   - Receive guidance based on official Tiger Data documentation

## Challenge Requirements Met

- ✅ Tiger Cloud service created and running
- ✅ Tiger CLI + MCP integration completed
- ✅ Dashboard screenshot submitted as proof

---

**Team:** Global Hack Week – Data  
**Date:** September 2026