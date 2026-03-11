# Otto's Expeditions

A sample Ascend project for the fictional Otto's Expeditions enterprise, demonstrating multi-platform data pipelines across BigQuery, Databricks, DuckDB, MotherDuck, and Snowflake.

## Project Structure

| Directory | Description |
|-----------|-------------|
| `automations/` | Event-driven and scheduled workflow triggers |
| `connections/` | Data plane and source connections |
| `data/` | Local CSV files for testing |
| `flows/` | Data pipelines organized by platform |
| `macros/` | Reusable Jinja SQL templates |
| `otto/` | AI agent configuration and customization |
| `profiles/` | Environment-specific parameters |
| `src/` | Shared Python modules |
| `templates/` | Simple Application templates |
| `vaults/` | External credential stores |

## Flows by Platform

Each platform has a consistent set of flows:

- **Extract-Load**: Ingest data from GCS and local files
- **Transform**: Business logic transformations
- **Metrics**: Aggregated analytics

Platforms: #flow:extract-load-bigquery, #flow:extract-load-databricks, #flow:extract-load-duckdb, #flow:extract-load-snowflake, #flow:extract-load-motherduck

## Getting Started

1. Create a workspace with an appropriate profile from `profiles/`
2. Configure your data plane connection parameters
3. Run the extract-load flow for your platform
4. Run the transform flow to process the data